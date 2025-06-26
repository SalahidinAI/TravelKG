from rest_framework import generics, viewsets
from .models import *
from .serializers import *


class CountryAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer


class RegionDetailAPIView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer


class RegionMealAPIView(generics.ListAPIView):
    queryset = RegionMeal.objects.all()
    serializer_class = RegionMealSerializer


class RegionPlaceListAPIView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = RegionPlaceSerializer

    def get_queryset(self):
        region_id = self.kwargs.get('region_id')
        return Place.objects.filter(region=region_id)


class HomePlaceAPIView(generics.ListAPIView):
    serializer_class = PlaceHomeSerializer

    def get_queryset(self):
        return Place.objects.filter(place_name='Bishkek')


class AbstractReviewAPIView(generics.ListAPIView):
    queryset = AbstractReview.objects.all()
    serializer_class = AbstractReviewSerializer


class ReviewPlaceAPIView(generics.ListAPIView):
    queryset = ReviewPlace.objects.all()
    serializer_class = ReviewPlaceSerializer


class ReviewPlaceLikeAPIView(generics.ListAPIView):
    queryset = ReviewPlaceLike.objects.all()
    serializer_class = ReviewPlaceLikeSerializer


class FavoriteAPIView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoritePlaceAPIView(generics.ListAPIView):
    queryset = FavoritePlace.objects.all()
    serializer_class = FavoritePlaceSerializer


class HotelAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class HotelImageAPIView(generics.ListAPIView):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer


class HotelHygieneAPIView(generics.ListAPIView):
    queryset = HotelHygiene.objects.all()
    serializer_class = HotelHygieneSerializer


class ReviewHotelAPIView(generics.ListAPIView):
    queryset = ReviewHotel.objects.all()
    serializer_class = ReviewHotelSerializer


class MealTypeAPIView(generics.ListAPIView):
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer


class SpecializedMenuAPIView(generics.ListAPIView):
    queryset = SpecializedMenu.objects.all()
    serializer_class = SpecializedMenuSerializer


class MealTimeAPIView(generics.ListAPIView):
    queryset = MealTime.objects.all()
    serializer_class = MealTimeSerializer


class RestaurantAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantImageAPIView(generics.ListAPIView):
    queryset = RestaurantImage.objects.all()
    serializer_class = RestaurantImageSerializer


class ReviewRestaurantAPIView(generics.ListAPIView):
    queryset = ReviewRestaurant.objects.all()
    serializer_class = ReviewRestaurantSerializer


class EventTypeAPIView(generics.ListAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class HomeAttractionAPIView(generics.ListAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionHomeSerializer


class CultureVarietyAPIView(generics.ListAPIView):
    queryset = CultureVariety.objects.all()
    serializer_class = CultureVarietySerializer


class HomeCultureAPIView(generics.ListAPIView):
    serializer_class = CultureHomeSerializer

    def get_queryset(self):
        return Culture.objects.filter(culture_variety__culture_variety_name='Home page')


# @api_view(['POST'])
# def toggle_book_like(request, book_id):
#     try:
#         book = Book.objects.get(id=book_id)
#     except Book.DoesNotExist:
#         return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     like, created = Like.objects.get_or_create(user=request.user, book=book)
#
#     if not created:
#         like.delete()
#         return Response({'detail': 'Like deleted'}, status=status.HTTP_404_NOT_FOUND)
#
#     return Response({'detail': 'Like created'}, status=status.HTTP_201_CREATED)