from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


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


class RegionMealInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = RegionMeal
    extra = 1


@admin.register(Region)
class RegionAdmin(TranslationAdmin, GeneralMedia):
    inlines = [RegionMealInline]


class AttractionInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Attraction
    extra = 1


class EventInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Event
    extra = 1


@admin.register(Place)
class PlaceAdmin(TranslationAdmin, GeneralMedia):
    inlines = [AttractionInline, EventInline]


class HotelHygieneInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = HotelHygiene
    extra = 1


class HotelContactInline(admin.TabularInline):
    model = HotelContact
    extra = 1


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


@admin.register(Hotel)
class HotelAdmin(TranslationAdmin, GeneralMedia):
    inlines = [HotelImageInline, HotelContactInline, HotelHygieneInline]


# @admin.register(HotelHygiene)
# class HotelHygieneAdmin(TranslationAdmin, GeneralMedia):
#     pass


@admin.register(MealType)
class MealTypeAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(SpecializedMenu)
class SpecializedMenuAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(MealTime)
class MealTimeAdmin(TranslationAdmin, GeneralMedia):
    pass


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(TranslationAdmin, GeneralMedia):
    inlines = [RestaurantImageInline]


@admin.register(EventType)
class EventTypeAdmin(TranslationAdmin, GeneralMedia):
    pass


class CultureInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Culture
    extra = 1


@admin.register(CultureVariety)
class CultureVarietyAdmin(TranslationAdmin, GeneralMedia):
    inlines = [CultureInline]


class ReviewPlaceLikeInline(admin.TabularInline):
    model = ReviewPlaceLike
    extra = 1


class ReviewPlaceAdmin(admin.ModelAdmin):
    inlines = [ReviewPlaceLikeInline]


class ReviewHotelLikeInline(admin.TabularInline):
    model = ReviewHotelLike
    extra = 1


class ReviewHotelAdmin(admin.ModelAdmin):
    inlines = [ReviewHotelLikeInline]


class ReviewRestaurantLikeInline(admin.TabularInline):
    model = ReviewRestaurantLike
    extra = 1


class ReviewRestaurantAdmin(admin.ModelAdmin):
    inlines = [ReviewRestaurantLikeInline]


class ReviewAttractionLikeInline(admin.TabularInline):
    model = ReviewAttractionLike
    extra = 1


class ReviewAttractionAdmin(admin.ModelAdmin):
    inlines = [ReviewAttractionLikeInline]


class FavoritePlaceInline(admin.TabularInline):
    model = FavoritePlace
    extra = 1


class FavoriteHotelInline(admin.TabularInline):
    model = FavoriteHotel
    extra = 1


class FavoriteRestaurantInline(admin.TabularInline):
    model = FavoriteHotel
    extra = 1


class FavoriteAttractionInline(admin.TabularInline):
    model = FavoriteHotel
    extra = 1


class FavoriteAdmin(admin.ModelAdmin):
    inlines = [FavoritePlaceInline, FavoriteHotelInline,
               FavoriteRestaurantInline, FavoriteAttractionInline]


admin.site.register(ReviewPlace, ReviewPlaceAdmin)
admin.site.register(ReviewHotel, ReviewHotelAdmin)
admin.site.register(ReviewRestaurant, ReviewRestaurantAdmin)
admin.site.register(ReviewAttraction, ReviewAttractionAdmin)


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(UserProfile)
# admin.site.register(HotelImage)
# admin.site.register(HotelContact)
# admin.site.register(RestaurantImage)
