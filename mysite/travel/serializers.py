from rest_framework import serializers
from django.utils import timezone
from .models import *

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


class RegionHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name', 'region_image']


class RegionMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionMeal
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


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
    class Meta:
        model = Attraction
        fields = ['id', 'title', 'description', 'image1']


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
