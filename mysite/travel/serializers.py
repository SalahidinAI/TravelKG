from rest_framework import serializers
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


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
#
#     def validate_birthday(self, value):
#         if value and value > timezone.now().date():
#             raise serializers.ValidationError("Birthday cannot be in the future.")
#         return value


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


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


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


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


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__'


class HotelHygieneSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelHygiene
        fields = '__all__'


class HotelContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelContact
        fields = '__all__'


class FavoriteHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteHotel
        fields = '__all__'


class ReviewHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHotel
        fields = '__all__'


class ReviewHotelLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHotelLike
        fields = '__all__'


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'


class SpecializedMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializedMenu
        fields = '__all__'


class MealTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealTime
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
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


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
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


class FavoriteAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAttraction
        fields = '__all__'


class CultureVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureVariety
        fields = '__all__'


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = '__all__'


class CultureHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'culture_name', 'image', 'description']

