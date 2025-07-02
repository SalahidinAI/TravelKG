from rest_framework import generics, viewsets, permissions
from .models import *
from .serializers import *
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerifyResetCodeSerializer
from rest_framework import generics, viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .coordinates import locations
from geopy.distance import geodesic
from drf_yasg.utils import swagger_auto_schema
from .permissions import UserEdit


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # <-- Это само вернёт 400 с деталями ошибок
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileEditSerializer
    permission_classes = [permissions.IsAuthenticated, UserEdit]


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


class ReviewPlaceCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewPlaceSerializer
    permissions_classes = [permissions.IsAuthenticated]


class ReviewPlaceDeleteAPIView(generics.DestroyAPIView):
    queryset = ReviewPlace.objects.all()
    serializer_class = ReviewPlaceSerializer
    permissions_classes = [permissions.IsAuthenticated, UserEdit]


class ReviewPlaceLikeAPIView(generics.ListAPIView):
    queryset = ReviewPlaceLike.objects.all()
    serializer_class = ReviewPlaceLikeSerializer


class FavoriteAPIView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoritePlaceAPIView(generics.ListAPIView):
    queryset = FavoritePlace.objects.all()
    serializer_class = FavoritePlaceSerializer


class PlaceListAPIView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceListSerializer


class PlaceDetailAPIView(generics.RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceDetailSerializer


class EventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        place_id = self.kwargs.get('place_id')
        return Event.objects.filter(place=place_id)


class AttractionListAPIView(generics.ListAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionListSerializer

    def get_queryset(self):
        place_id = self.kwargs.get('place_id')
        return Attraction.objects.filter(place=place_id)


class AttractionDetailAPIView(generics.RetrieveAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionDetailSerializer


class RestaurantListAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        place_id = self.kwargs.get('place_id')
        return Restaurant.objects.filter(place=place_id)


class RestaurantDetailAPIView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer


class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer

    def get_queryset(self):
        place_id = self.kwargs.get('place_id')
        return Hotel.objects.filter(place=place_id)


class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer


class ReviewHotelCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewHotelSerializer
    permissions_classes = [permissions.IsAuthenticated]


class ReviewHotelDeleteAPIView(generics.DestroyAPIView):
    queryset = ReviewHotel.objects.all()
    serializer_class = ReviewHotelSerializer
    permissions_classes = [permissions.IsAuthenticated, UserEdit]


class ReviewHotelListAPIView(generics.ListAPIView):
    queryset = ReviewHotel.objects.all()
    serializer_class = ReviewHotelListSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return ReviewHotel.objects.filter(hotel=hotel_id)


class ReviewRestaurantCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewRestaurantSerializer
    permissions_classes = [permissions.IsAuthenticated]


class ReviewRestaurantDeleteAPIView(generics.DestroyAPIView):
    queryset = ReviewRestaurant.objects.all()
    serializer_class = ReviewRestaurantSerializer
    permissions_classes = [permissions.IsAuthenticated, UserEdit]


class ReviewAttractionCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewAttractionSerializer
    permissions_classes = [permissions.IsAuthenticated]


class ReviewAttractionDeleteAPIView(generics.DestroyAPIView):
    queryset = ReviewAttraction.objects.all()
    permissions_classes = [permissions.IsAuthenticated, UserEdit]


class HomeAttractionAPIView(generics.ListAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionHomeSerializer


class HomeCultureAPIView(generics.ListAPIView):
    serializer_class = CultureHomeSerializer

    def get_queryset(self):
        return Culture.objects.filter(culture_variety__culture_variety_name='Home page')


class GalleryListAPIView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = GalleryListSerializer


class CultureListAPIView(generics.ListAPIView):
    queryset = CultureVariety.objects.all()
    serializer_class = CultureListSerializer


class CultureDetailAPIView(generics.RetrieveAPIView):
    queryset = CultureVariety.objects.all()
    serializer_class = CultureDetailSerializer


@api_view(['POST'])
def toggle_review_place_like(request, review_place_id):
    try:
        review_place = ReviewPlace.objects.get(id=review_place_id)
    except ReviewPlace.DoesNotExist:
        return Response({'detail': 'Place review not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = ReviewPlaceLike.objects.get_or_create(user=request.user, review_place=review_place)

    if not created:
        like.delete()
        return Response({'detail': 'Like is deleted'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Like is created'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def toggle_review_hotel_like(request, review_hotel_id):
    try:
        review_hotel = ReviewHotel.objects.get(id=review_hotel_id)
    except ReviewHotel.DoesNotExist:
        return Response({'detail': 'Hotel review not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = ReviewHotelLike.objects.get_or_create(user=request.user, review_hotel=review_hotel)

    if not created:
        like.delete()
        return Response({'detail': 'Like is deleted'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Like is created'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def toggle_review_restaurant_like(request, review_restaurant_id):
    try:
        restaurant = ReviewRestaurant.objects.get(id=review_restaurant_id)
    except ReviewRestaurant.DoesNotExist:
        return Response({'detail': 'Restaurant review not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = ReviewRestaurantLike.objects.get_or_create(user=request.user, restaurant=restaurant)

    if not created:
        like.delete()
        return Response({'detail': 'Like is deleted'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Like is created'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def toggle_review_attraction_like(request, review_attraction_id):
    try:
        attraction = ReviewAttraction.objects.get(id=review_attraction_id)
    except ReviewAttraction.DoesNotExist:
        return Response({'detail': 'Attraction review not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = ReviewAttractionLike.objects.get_or_create(user=request.user, attraction=attraction)

    if not created:
        like.delete()
        return Response({'detail': 'Like is deleted'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Like is created'}, status=status.HTTP_201_CREATED)


# travel/views.py

class TravelDistanceAPIView(APIView):
    @swagger_auto_schema(request_body=TravelRequestSerializer)  # 👈 ЭТО ВАЖНО
    def post(self, request):
        serializer = TravelRequestSerializer(data=request.data)
        if serializer.is_valid():
            from_city = serializer.validated_data['from_city']
            to_city = serializer.validated_data['to_city']

            coord_from = locations.get(from_city)
            coord_to = locations.get(to_city)

            if not coord_from or not coord_to:
                return Response({"error": "Unknown city name"}, status=status.HTTP_400_BAD_REQUEST)

            distance = geodesic(coord_from, coord_to).km

            return Response({
                "from": from_city,
                "to": to_city,
                "distance_km": round(distance, 2),
                "time": {
                    "walking_hours": round(distance / 5, 2),
                    "driving_hours": round(distance / 70, 2),
                    "train_hours": round(distance / 80, 2),
                    "plane_hours": round(distance / 600, 2)
                }
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
