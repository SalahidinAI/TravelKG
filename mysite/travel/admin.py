from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class GeneralMedia:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Country)
class CountryAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(City)
class CityAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Region)
class RegionAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(RegionMeal)
class RegionMealAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Place)
class PlaceAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Hotel)
class HotelAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(HotelHygiene)
class HotelHygieneAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(MealType)
class MealTypeAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(SpecializedMenu)
class SpecializedMenuAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(MealTime)
class MealTimeAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(EventType)
class EventTypeAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Event)
class EventAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Attraction)
class AttractionAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(CultureVariety)
class CultureVarietyAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Culture)
class CultureAdmin(TranslationAdmin, GeneralMedia):
    pass


admin.site.register(UserProfile)
admin.site.register(AbstractReview)
admin.site.register(ReviewPlace)
admin.site.register(ReviewPlaceLike)
admin.site.register(Favorite)
admin.site.register(FavoritePlace)
admin.site.register(HotelImage)
admin.site.register(HotelContact)
admin.site.register(FavoriteHotel)
admin.site.register(ReviewHotel)
admin.site.register(ReviewHotelLike)
admin.site.register(RestaurantImage)
admin.site.register(ReviewRestaurant)
admin.site.register(ReviewRestaurantLike)
admin.site.register(ReviewAttraction)
admin.site.register(ReviewAttractionLike)
