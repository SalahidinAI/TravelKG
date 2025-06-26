from rest_framework.urls import path
from .views import *


urlpatterns = [
    path('attraction_review_like/<int:review_attraction_id>/', toggle_review_attraction_like, name='review_attraction_like'),

    path("distance/", TravelDistanceAPIView.as_view(), name="distance"),

    path('home/place/', HomePlaceAPIView.as_view(), name='home_place_list'),
    path('home/attraction/', HomeAttractionAPIView.as_view(), name='home_attraction_list'),
    path('home/culture/', HomeCultureAPIView.as_view(), name='home_culture_list'),
    path('region/', RegionListAPIView.as_view(), name='region_list'),

    path('region/<int:pk>/', RegionDetailAPIView.as_view(), name='region_detail'),
    path('region/<int:pk>/meal/', RegionMealAPIView.as_view(), name='region_detail_meal'),
    path('region/<int:region_id>/place/', RegionPlaceListAPIView.as_view(), name='region_detail_place_list'),
]
