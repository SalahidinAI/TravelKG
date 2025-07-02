from rest_framework.urls import path
from .views import *
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from travel.views import verify_reset_code


urlpatterns = [
    path('attraction_review_like/<int:review_attraction_id>/', toggle_review_attraction_like,
         name='review_attraction_like'),
    path('place_review_like/<int:review_place_id>/', toggle_review_place_like, name='review_place_like'),
    path('hotel_review_like/<int:review_hotel_id>/', toggle_review_hotel_like, name='review_hotel_like'),
    path('restaurant_review_like/<int:review_restaurant_id>/', toggle_review_restaurant_like,
         name='review_restaurant_like'),

    path("distance/", TravelDistanceAPIView.as_view(), name="distance"),

    path('home/place/', HomePlaceAPIView.as_view(), name='home_place_list'),
    path('home/attraction/', HomeAttractionAPIView.as_view(), name='home_attraction_list'),
    path('home/culture/', HomeCultureAPIView.as_view(), name='home_culture_list'),
    path('region/', RegionListAPIView.as_view(), name='region_list'),


    path('place/', PlaceListAPIView.as_view(), name='place_list'),
    path('place/<int:pk>/', PlaceDetailAPIView.as_view(), name='place_detail'),
    path('event/', EventAPIView.as_view(), name='event_list'),
    path('attraction/', AttractionListAPIView.as_view(), name='attraction_list'),
    path('attraction/<int:pk>/', AttractionDetailAPIView.as_view(), name='attraction_detail'),
    path('restaurant/', RestaurantListAPIView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/', RestaurantDetailAPIView.as_view(), name='restaurant_detail'),
    path('hotel/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),

    path('culture/', CultureAPIView.as_view(), name='culture_list'),


    path('region/<int:pk>/', RegionDetailAPIView.as_view(), name='region_detail'),
    path('region/<int:pk>/meal/', RegionMealAPIView.as_view(), name='region_detail_meal'),
    path('region/<int:region_id>/place/', RegionPlaceListAPIView.as_view(), name='region_detail_place_list'),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_detail'),

    path('review_attraction/create', ReviewAttractionCreateAPIView.as_view(), name='review_attraction_create'),
    path('review_attraction/delete/<int:pk>/', ReviewAttractionDeleteAPIView.as_view(), name='review_attraction_delete'),
    path('review_attraction/<int:attraction_id>/', ReviewAttractionListAPIView.as_view(), name='review_attraction_list'),

    path('review_restaurant/create', ReviewRestaurantCreateAPIView.as_view(), name='review_restaurant_create'),
    path('review_restaurant/delete/<int:pk>/', ReviewRestaurantDeleteAPIView.as_view(), name='review_restaurant_delete'),
    path('review_restaurant/<int:restaurant_id>/', ReviewRestaurantListAPIView.as_view(), name='review_restaurant_list'),

    path('review_hotel/create', ReviewHotelCreateAPIView.as_view(), name='review_hotel_create'),
    path('review_hotel/delete/<int:pk>/', ReviewHotelDeleteAPIView.as_view(), name='review_hotel_delete'),
    path('review_hotel/<int:hotel_id>/', ReviewHotelListAPIView.as_view(), name='review_hotel_list'),

    path('review_place/create', ReviewPlaceCreateAPIView.as_view(), name='review_place_create'),
    path('review_place/delete/<int:pk>/', ReviewPlaceDeleteAPIView.as_view(), name='review_place_delete'),
    path('review_place/<int:place_id>/', ReviewPlaceListAPIView.as_view(), name='review_place_list'),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_detail'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),

]
