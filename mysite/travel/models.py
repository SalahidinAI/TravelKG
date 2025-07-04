from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


TEMPERATURE_CHOICES = [
    (i, str(i)) for i in range(-50, 50)
]


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.country_name


class City(models.Model):
    city_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.city_name}'


# add restriction to birthday
class UserProfile(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos/')
    banner = models.ImageField(upload_to='banner_photo/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

    def clean(self):
        super().clean()
        if self.birthday and self.birthday > timezone.now().date():
            raise ValidationError({'birthday': "Birthday can't be in the future."})



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Укажи свой реальный домен
    frontend_url = "https://example.com"  # Заменить на адрес твоего сайта или фронтенда

    # Генерация полного URL сброса пароля
    reset_url = "{}{}?token={}".format(
        frontend_url,
        reverse('password_reset:reset-password-request'),  # Django-обработчик, можно заменить
        reset_password_token.key
    )

    # Отправка письма
    send_mail(
        subject="Password Reset for Some Website",  # Тема
        message=f"Use the following link to reset your password:\n{reset_url}",  # Текст
        from_email="noreply@example.com",  # Отправитель
        recipient_list=[reset_password_token.user.email],  # Получатель
        fail_silently=False,
    )


# Add reset password logic


class Region(models.Model):
    region_name = models.CharField(max_length=32, unique=True)
    region_image = models.ImageField(upload_to='region_images/')
    description = models.TextField()
    temperature = models.SmallIntegerField(choices=TEMPERATURE_CHOICES)

    def __str__(self):
        return self.region_name


class RegionMeal(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=32, unique=True)
    description = models.TextField()
    meal_image1 = models.ImageField(upload_to='meal_images/')
    meal_image2 = models.ImageField(upload_to='meal_images/')
    meal_image3 = models.ImageField(upload_to='meal_images/')

    def __str__(self):
        return f'{self.region} {self.meal_name}'


# def function
class Place(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=64, unique=True)
    place_image = models.ImageField(upload_to='place_images/')
    description = models.TextField()
    temperature = models.SmallIntegerField(choices=TEMPERATURE_CHOICES)

    def __str__(self):
        return f'{self.region} {self.place_name}'

    def get_avg_rating(self):
        all_reviews = self.place_reviews.all()
        scores = [i.service_score for i in all_reviews if i.service_score]
        if scores:
            return sum(scores) / len(scores)
        return 0

    def get_count_reviews(self):
        all_reviews = self.place_reviews.all()
        return all_reviews.count()

    def get_level_rating(self):
        all_reviews = self.place_reviews.all()
        ratings = [i.service_score for i in all_reviews if i.service_score]
        return {
            'excellent': ratings.count(5),
            'good': ratings.count(4),
            'not_bad': ratings.count(3),
            'bad': ratings.count(2),
            'terribly': ratings.count(1),
        }


# class PlaceMap(models.Model):
#     place =  models.ForeignKey(Place, on_delete=models.CASCADE)

# not finished


# add filter to review
class AbstractReview(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    service_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    photo1 = models.ImageField(upload_to='review_photos/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='review_photos/', null=True, blank=True)
    photo3 = models.ImageField(upload_to='review_photos/', null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.service_score}'

    def clean(self):
        super().clean()
        if not self.text and not self.service_score:
            raise ValidationError('Both text and service_score can not be null')


class ReviewPlace(AbstractReview):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.place} {self.user}'


class ReviewPlaceLike(models.Model):
    review_place = models.ForeignKey(ReviewPlace, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review_place} {self.user}'

    class Meta:
        unique_together = ('review_place', 'user')


# logic not finished, add perform create
class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    # class Meta:
    # ordering = 'created_date'
    #         check ordering, is it working well


# function > quantity of photos
class FavoritePlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.place} {self.favorite}'

    class Meta:
        unique_together = ('place', 'favorite')


# add restriction to prices low < high
class Hotel(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=64)
    low_price = models.PositiveSmallIntegerField()
    high_price = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    cars = models.PositiveSmallIntegerField(default=0)
    bikes = models.PositiveSmallIntegerField(default=0)
    pets = models.PositiveSmallIntegerField(default=0)
    address = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    kitchen = models.BooleanField(default=False)
    air = models.BooleanField(default=False)
    washer = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    hair_dryer = models.BooleanField(default=False)
    towel = models.BooleanField(default=False)
    iron = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.hotel_name} {self.owner}'

    def clean(self):
        super().clean()
        if self.low_price > self.high_price:
            raise ValidationError("'low_price' can't be higher than 'high_price'")

    def get_avg_rating(self):
        all_reviews = self.review_hotel.all()
        if all_reviews.exists():
            ratings = [i.service_score for i in all_reviews if i.service_score]
            return sum(ratings) / len(ratings)
        return 0

    def get_count_review(self):
        all_reviews = self.review_hotel.all()
        return len(all_reviews)

    def get_level_rating(self):
        all_reviews = self.review_hotel.all()
        ratings = [i.service_score for i in all_reviews if i.service_score]
        return {
            'excellent': ratings.count(5),
            'good': ratings.count(4),
            'not_bad': ratings.count(3),
            'bad': ratings.count(2),
            'terribly': ratings.count(1),
        }


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f'{self.hotel}'


class HotelHygiene(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_hygiene')
    hygiene_title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.hotel} {self.hygiene_title}'


class HotelContact(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_contacts')
    hotel_contact = PhoneNumberField(unique=True)

    def __str__(self):
        return f'{self.hotel} {self.hotel_contact}'


class FavoriteHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel} {self.favorite}'

    class Meta:
        unique_together = ('hotel', 'favorite')


# add filter to review
class ReviewHotel(AbstractReview):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='review_hotel')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hotel} {self.user}'


class ReviewHotelLike(models.Model):
    review_hotel = models.ForeignKey(ReviewHotel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review_hotel} {self.user}'

    class Meta:
        unique_together = ('review_hotel', 'user')


class MealType(models.Model):
    meal_type = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.meal_type


class SpecializedMenu(models.Model):
    specialized_menu = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.specialized_menu


class MealTime(models.Model):
    meal_time = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.meal_time


# add restriction to prices
class Restaurant(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=64)
    low_price = models.PositiveSmallIntegerField()
    high_price = models.PositiveSmallIntegerField()
    meal_type = models.ManyToManyField(MealType)
    specialized_menu = models.ManyToManyField(SpecializedMenu)
    meal_time = models.ManyToManyField(MealTime)
    address = models.CharField(max_length=128, unique=True)
    phone = PhoneNumberField(unique=True)

    def __str__(self):
        return f'{self.place} {self.restaurant_name}'

    def clean(self):
        super().clean()
        if self.low_price > self.high_price:
            raise ValidationError("'low_price' can't be higher than 'high_price'")

    def get_total_images(self):
        all_images = self.restaurant_images.all()
        return len(all_images)

    def get_rating(self):
        all_reviews = self.review_restaurant.all()
        if all_reviews.exists():
            all_stars = []
            for i in all_reviews:
                if i.nutrition_score:
                    all_stars.append(i.nutrition_score)
                if i.price_score:
                    all_stars.append(i.price_score)
                if i.atmosphere_score:
                    all_stars.append(i.atmosphere_score)
                if i.service_score:
                    all_stars.append(i.service_score)
            return {
                'avg_rating': sum(all_stars) / len(all_stars) ,
                'all_reviews': len(all_stars),
                    }
        return 0

    def get_level_rating(self):
        all_reviews = self.review_restaurant.all()
        dic = {
            1: [], 2: [], 3: [], 4: [], 5: [],
        }
        for i in all_reviews:
            service_score = i.service_score
            if service_score in dic:
                dic[service_score].append(service_score)

            price_score = i.price_score
            if price_score in dic:
                dic[price_score].append(price_score)

            nutrition_score = i.nutrition_score
            if nutrition_score in dic:
                dic[nutrition_score].append(nutrition_score)

            atmosphere_score = i.atmosphere_score
            if atmosphere_score in dic:
                dic[atmosphere_score].append(atmosphere_score)
        return {
            'excellent': sum(dic[5]),
            'good': sum(dic[4]),
            'not_bad': sum(dic[3]),
            'bad': sum(dic[2]),
            'terribly': sum(dic[1]),
        }


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_images')
    restaurant_image = models.ImageField(upload_to='restaurant_images/')

    def __str__(self):
        return f'{self.restaurant}'


class FavoriteRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.restaurant} {self.favorite}'

    class Meta:
        unique_together = ('restaurant', 'favorite')


# check,p Are scores working well?
class ReviewRestaurant(AbstractReview):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='review_restaurant')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    nutrition_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    price_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    atmosphere_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.restaurant} {self.user}'


class ReviewRestaurantLike(models.Model):
    restaurant = models.ForeignKey(ReviewRestaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.restaurant} {self.user}'

    class Meta:
        unique_together = ('restaurant', 'user')


class EventType(models.Model):
    event_type = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.event_type}'


class Event(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_events')
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_image/')
    title = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateField()
    ticket = models.BooleanField(default=True)
    address = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.place} {self.event_type}'


# def review quantity / avg review
class Attraction(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_attractions')
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    country = models.ManyToManyField(Country)
    low_price = models.PositiveSmallIntegerField()
    high_price = models.PositiveSmallIntegerField()
    image1 = models.ImageField(upload_to='attraction_images/')
    image2 = models.ImageField(upload_to='attraction_images/')
    image3 = models.ImageField(upload_to='attraction_images/')
    image4 = models.ImageField(upload_to='attraction_images/')

    def __str__(self):
        return f'{self.place} {self.title}'

    def get_total_reviews(self):
        total_reviews = self.review_attraction.all()
        return total_reviews.count()

    def get_avg_review(self):
        all_reviews = self.review_attraction.all()
        if all_reviews.exists():
            return sum([i.service_score for i in all_reviews if i.service_score]) / all_reviews.count()
        return 0

    def get_level_rating(self):
        all_reviews = self.review_attraction.all()
        ratings = [i.service_score for i in all_reviews if i.service_score]
        return {
            'excellent': ratings.count(5),
            'good': ratings.count(4),
            'not_bad': ratings.count(3),
            'bad': ratings.count(2),
            'terribly': ratings.count(1),
        }


# function
class ReviewAttraction(AbstractReview):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='review_attraction')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attraction} {self.user}'


class ReviewAttractionLike(models.Model):
    attraction = models.ForeignKey(ReviewAttraction, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attraction} {self.user}'

    class Meta:
        unique_together = ('attraction', 'user')


class FavoriteAttraction(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.attraction} {self.favorite}'

    class Meta:
        unique_together = ('attraction', 'favorite')


class CultureVariety(models.Model):
    culture_variety_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.culture_variety_name


class Culture(models.Model):
    culture_variety = models.ForeignKey(CultureVariety, on_delete=models.CASCADE, related_name='cultures')
    culture_name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='culture_images/')
    description = models.TextField()

    def __str__(self):
        return f'{self.culture_variety} {self.culture_name}'
