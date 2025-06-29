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

    # path('country/', CountryAPIView.as_view(), name='country_list'),
    # path('city/', CityAPIView.as_view(), name='city_list'),
    # path('user/', UserProfileAPIView.as_view(), name='user_list'),
    # path('abstract_review/', AbstractReviewAPIView.as_view(), name='abstract_review_list'),
    # path('review_place/', ReviewPlaceAPIView.as_view(), name='review_place_list'),
    # path('review_place_like/', ReviewPlaceLikeAPIView.as_view(), name='review_place_like_list'),
    # path('favorite/', FavoriteAPIView.as_view(), name='favorite_list'),
    # path('favorite_place/', FavoritePlaceAPIView.as_view(), name='favorite_place_list'),
    # path('hotel/', HotelAPIView.as_view(), name='hotel_list'),
    # path('hotel_image/', HotelImageAPIView.as_view(), name='hotel_image_list'),
    # path('hotel_hygiene/', HotelHygieneAPIView.as_view(), name='hotel_hygiene_list'),
    # path('review_hotel/', ReviewHotelAPIView.as_view(), name='review_hotel_list'),
    # path('meal_type/', MealTypeAPIView.as_view(), name='meal_type_list'),
    # path('specialized_menu/', SpecializedMenuAPIView.as_view(), name='specialized_menu_list'),
    # path('meal_time/', MealTimeAPIView.as_view(), name='meal_time_list'),
    # path('restaurant/', RestaurantAPIView.as_view(), name='restaurant_list'),
    # path('restaurant_image/', RestaurantImageAPIView.as_view(), name='restaurant_image_list'),
    # path('review_restaurant/', ReviewRestaurantAPIView.as_view(), name='review_restaurant_list'),
    # path('event_type/', EventTypeAPIView.as_view(), name='event_type_list'),
    # path('event/', EventAPIView.as_view(), name='event_list'),
    # path('culture_variety/', CultureVarietyAPIView.as_view(), name='culture_variety'),


    path('region/<int:pk>/', RegionDetailAPIView.as_view(), name='region_detail'),
    path('region/<int:pk>/meal/', RegionMealAPIView.as_view(), name='region_detail_meal'),
    path('region/<int:region_id>/place/', RegionPlaceListAPIView.as_view(), name='region_detail_place_list'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]

urlpatterns += [
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
]