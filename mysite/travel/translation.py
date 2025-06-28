from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name', 'description')


@register(RegionMeal)
class RegionMealTranslationOptions(TranslationOptions):
    fields = ('meal_name', 'description')


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('place_name', 'description')


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'address', 'description')


@register(HotelHygiene)
class HotelHygieneTranslationOptions(TranslationOptions):
    fields = ('hygiene_title',)


@register(MealType)
class MealTypeTranslationOptions(TranslationOptions):
    fields = ('meal_type',)


@register(SpecializedMenu)
class SpecializedMenuTranslationOptions(TranslationOptions):
    fields = ('specialized_menu',)


@register(MealTime)
class MealTimeTranslationOptions(TranslationOptions):
    fields = ('meal_time',)


@register(Restaurant)
class RestaurantTranslationOptions(TranslationOptions):
    fields = ('restaurant_name', 'address')


@register(EventType)
class EventTypeTranslationOptions(TranslationOptions):
    fields = ('event_type',)


@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')


@register(Attraction)
class AttractionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(CultureVariety)
class CultureVarietyTranslationOptions(TranslationOptions):
    fields = ('culture_variety_name',)


@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('culture_name', 'description')


# @register()
# class TranslationOptions(TranslationOptions):
#     fields = ('',)
