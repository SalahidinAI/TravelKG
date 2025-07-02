from rest_framework import serializers, generics
from django.utils import timezone
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django_rest_passwordreset.models import ResetPasswordToken
from phonenumber_field.serializerfields import PhoneNumberField
from datetime import date

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'password', 'confirm_password',
            'username', 'last_name', 'phone_number', 'birthday'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Пароль должен быть не менее 6 символов.")
        return value

    def validate_birthday(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Дата рождения не может быть в будущем.")
        return value

    def validate_phone_number(self, value):
        if value and User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Этот номер уже используется.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль")

        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        reset_code = data.get('reset_code')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают.")

        try:
            token = ResetPasswordToken.objects.get(user__email=email, key=str(reset_code))
        except ResetPasswordToken.DoesNotExist:
            raise serializers.ValidationError("Неверный код сброса или email.")

        data['user'] = token.user
        data['token'] = token
        return data

    def save(self):
        user = self.validated_data['user']
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        # Удаляем использованный токен
        token.delete()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'last_name', 'country', 'city']


class UserProfileListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'last_name', 'country', 'city', 'profile_photo',
                  'banner']


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'last_name', 'country', 'city', 'profile_photo',
                  'banner', 'email', 'password', 'phone_number', 'birthday']

    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if UserProfile.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def validate_birthday(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата рождения не может быть в будущем.")
        return value


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
#
#     def validate_birthday(self, value):
#         if value and value > timezone.now().date():
#             raise serializers.ValidationError("Birthday cannot be in the future.")
#         return value


class TravelRequestSerializer(serializers.Serializer):
    from_city = serializers.CharField()
    to_city = serializers.CharField()


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name', 'region_image']


class RegionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name', 'region_image', 'description', 'temperature']


class RegionMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionMeal
        fields = ['id', 'meal_name', 'description', 'meal_image1', 'meal_image2', 'meal_image3']


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'place_name', 'place_image']


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'event_type']


class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer()

    class Meta:
        model = Event
        fields = ['id', 'event_type', 'image', 'title', 'description', 'date', 'ticket', 'address']


class AttractionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'title', 'image1']


class ReviewPlaceListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = ReviewPlace
        fields = ['id', 'user', 'service_score', 'photo1', 'photo2', 'photo3',
                  'text', 'parent', 'created_date']


class PlaceDetailSerializer(serializers.ModelSerializer):
    place_reviews = ReviewPlaceListSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_reviews = serializers.SerializerMethodField()
    level_rating = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'place_name', 'place_image', 'description', 'temperature',
                  'avg_rating', 'count_reviews', 'level_rating', 'place_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()

    def get_level_rating(self, obj):
        return obj.get_level_rating()


class ReviewAttractionListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = ReviewAttraction
        fields = ['id', 'user', 'parent', 'service_score', 'text',
                  'photo1', 'photo2', 'photo3', 'created_date']


class AttractionDetailSerializer(serializers.ModelSerializer):
    review_attraction = ReviewAttractionListSerializer(many=True, read_only=True)
    total_reviews = serializers.SerializerMethodField()
    avg_review = serializers.SerializerMethodField()
    level_rating = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = ['id', 'title', 'description', 'image1', 'image2', 'image3', 'image4',
                  'total_reviews', 'avg_review', 'level_rating', 'review_attraction']

    def get_total_reviews(self, obj):
        return obj.get_total_reviews()

    def get_avg_review(self, obj):
        return obj.get_avg_review()

    def get_level_rating(self, obj):
        return obj.get_level_rating()


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ['id', 'meal_type']


class SpecializedMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializedMenu
        fields = ['id', 'specialized_menu']


class MealTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealTime
        fields = ['id', 'meal_time']


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ['id', 'restaurant_image']


class RestaurantListSerializer(serializers.ModelSerializer):
    restaurant_images = RestaurantImageSerializer(read_only=True, many=True)
    meal_type = MealTypeSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    total_images = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_images', 'restaurant_name', 'meal_type', 'low_price', 'high_price',
                  'total_images', 'rating']

    def get_total_images(self, obj):
        return obj.get_total_images()

    def get_rating(self, obj):
        return obj.get_rating()


class ReviewRestaurantListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = ReviewRestaurant
        fields = ['id', 'user', 'photo1', 'photo2', 'photo3', 'text', 'service_score', 'nutrition_score', 'price_score',
                  'atmosphere_score', 'parent', 'created_date']


class RestaurantDetailSerializer(serializers.ModelSerializer):
    restaurant_images = RestaurantImageSerializer(read_only=True, many=True)
    meal_type = MealTypeSerializer(many=True)
    specialized_menu = SpecializedMenuSerializer(many=True)
    meal_time = MealTimeSerializer(many=True)
    review_restaurant = ReviewRestaurantListSerializer(read_only=True, many=True)
    total_images = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    level_rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_images', 'restaurant_name', 'low_price', 'high_price', 'meal_type',
                  'specialized_menu', 'meal_time', 'address', 'phone', 'total_images', 'rating', 'level_rating', 'review_restaurant']

    def get_total_images(self, obj):
        return obj.get_total_images()

    def get_rating(self, obj):
        return obj.get_rating()

    def get_level_rating(self, obj):
        return obj.get_level_rating()


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'hotel_image']


class HotelListSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(read_only=True, many=True)
    avg_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_images', 'hotel_name', 'avg_rating', 'count_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_review(self, obj):
        return obj.get_count_review()


class HotelHygieneSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelHygiene
        fields = ['id', 'hygiene_title']


class HotelContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelContact
        fields = ['id', 'hotel_contact']


class ReviewHotelListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = ReviewHotel
        fields = ['id', 'user', 'service_score', 'photo1', 'photo2', 'photo3',
                  'text', 'parent', 'created_date']


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(read_only=True, many=True)
    hotel_hygiene = HotelHygieneSerializer(read_only=True, many=True)
    owner = UserProfileSimpleSerializer()
    hotel_contacts = HotelContactSerializer(read_only=True, many=True)
    avg_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()
    level_rating = serializers.SerializerMethodField()
    review_hotel = ReviewHotelListSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'owner', 'hotel_images', 'hotel_name', 'low_price', 'high_price', 'bedrooms', 'bathrooms',
                  'cars', 'bikes', 'pets', 'address', 'description', 'kitchen', 'air', 'washer', 'tv', 'wifi',
                  'balcony', 'parking', 'hair_dryer', 'towel', 'iron', 'hotel_hygiene', 'hotel_contacts',
                  'avg_rating', 'count_review', 'level_rating', 'review_hotel']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_review(self, obj):
        return obj.get_count_review()

    def get_level_rating(self, obj):
        return obj.get_level_rating()


class CultureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureVariety
        fields = ['id', 'culture_variety_name']


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'culture_name', 'image', 'description']


class CultureDetailSerializer(serializers.ModelSerializer):
    cultures = CultureSerializer(many=True, read_only=True)

    class Meta:
        model = CultureVariety
        fields = ['id', 'culture_variety_name', 'cultures']


class RegionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name']


class RegionPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'place_name', 'place_image']


class PlaceHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'place_name', 'place_image', 'description']


class AbstractReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractReview
        fields = '__all__'


class ReviewPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPlace
        fields = '__all__'


class ReviewPlaceLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPlaceLike
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoritePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePlace
        fields = '__all__'


class FavoriteHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteHotel
        fields = '__all__'


class ReviewHotelLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHotelLike
        fields = '__all__'


class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRestaurant
        fields = '__all__'


class ReviewRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRestaurant
        fields = '__all__'


class ReviewRestaurantLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRestaurantLike
        fields = '__all__'


class AttractionHomeSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    avg_review = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = ['id', 'title', 'description', 'image1', 'total_reviews', 'avg_review']

    def get_total_reviews(self, obj):
        return obj.get_total_reviews()

    def get_avg_review(self, obj):
        return obj.get_avg_review()


class ReviewAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAttraction
        fields = '__all__'


class ReviewAttractionLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAttractionLike
        fields = '__all__'


class ReviewHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHotel
        fields = '__all__'


class FavoriteAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAttraction
        fields = '__all__'


class CultureHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'culture_name', 'image', 'description']


class GalleryListSerializer(serializers.ModelSerializer):
    region = RegionTitleSerializer()
    avg_rating = serializers.SerializerMethodField()
    count_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'place_name', 'place_image', 'region', 'avg_rating', 'count_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()
