from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


TEMPERATURE_CHOICES = (
    (i, str(i)) for i in range(-50, 50)
)


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)


class City(models.Model):
    city_name = models.CharField(max_length=64, unique=True)


# add restriction to birthday
class UserProfile(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos/')
    bg_photo = models.ImageField(upload_to='user_bg_photo/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)


# Add reset password logic


class Region(models.Model):
    region_name = models.CharField(max_length=32, unique=True)
    region_image = models.ImageField(upload_to='region_images/')
    description = models.TextField()
    temperature = models.PositiveSmallIntegerField(choices=TEMPERATURE_CHOICES, null=True, blank=True)


class RegionMeal(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=32, unique=True)
    description = models.TextField()
    meal_image1 = models.ImageField(upload_to='meal_images/')
    meal_image2 = models.ImageField(upload_to='meal_images/')
    meal_image3 = models.ImageField(upload_to='meal_images/')
# check this description's logic, may be u neet to divide it by 2


class Place(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=64, unique=True)
    place_image = models.ImageField(upload_to='place_images/')
    description = models.TextField()
    temperature = models.PositiveSmallIntegerField(choices=TEMPERATURE_CHOICES, null=True, blank=True)
    # place's logic is not finished


class CultureVariety(models.Model):
    culture_variety_name = models.CharField(max_length=64, unique=True)


class Culture(models.Model):
    culture_variety = models.ForeignKey(CultureVariety, on_delete=models.CASCADE)
    culture_name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='culture_images/')
    description = models.TextField()
# may be we need to change this logic, relationship to each paragraph



