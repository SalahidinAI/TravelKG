from rest_framework.urls import path
from .views import *


urlpatterns = [
    path('home/place/', HomePlaceAPIView.as_view(), name='home_place_list'),
    path('home/attraction/', HomeAttractionAPIView.as_view(), name='home_attraction_list'),
    path('home/culture/', HomeCultureAPIView.as_view(), name='home_culture_list'),
    path('home/region/', HomeRegionAPIView.as_view(), name='home_region_list'),
]