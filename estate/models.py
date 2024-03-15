from unicodedata import name
from django.db import models
from categories.models import CityModel, RegionCityModel, VillageModel
from django.utils import timezone

from infousers.models import InfoUserModel

# Create your models here.

SOCIAL_MEDIA = (
    ("edareAndTejari", "اداری و تجاری"),
    ("masconi", "مسکونی"),

)


# SOCIAL_MEDIA = (
#     ("اداری و تجاری", "edareAndTejari"),
#     ("مسکونی", "masconi"),

# )


class TypeEstateModel(models.Model):
    typeestate = models.CharField(
        max_length=100, choices=SOCIAL_MEDIA, verbose_name='نوع')
    name = models.CharField(max_length=100, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'نوع ملک'
        verbose_name_plural = 'نوع ملک ها'


class ProductsEstateModel(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام')
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')
    village = models.ForeignKey(
        VillageModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name='روستا')

    region = models.ForeignKey(
        RegionCityModel, on_delete=models.CASCADE, null=True, blank=True)

    price = models.BigIntegerField(null=True, verbose_name='قیمت')
    rent = models.BigIntegerField(null=True, verbose_name='اجاره')
    mortgage = models.BigIntegerField(null=True, verbose_name='رهن')

    address = models.TextField(verbose_name='آدرس')

    infouser = models.ForeignKey(
        InfoUserModel, on_delete=models.CASCADE, verbose_name='صنف')
    image = models.ImageField(
        upload_to='ImageEstatePreview', verbose_name='تصویر')
    description = models.TextField(null=True, verbose_name='توضیحات')
    year = models.IntegerField(verbose_name='سال ساخت')
    BuildingArea = models.IntegerField(verbose_name='متراژ بنا')
    LanArea = models.IntegerField(verbose_name='متراژ زمین')

    parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    warehouse = models.BooleanField(default=False, verbose_name='انباری')
    balcony = models.BooleanField(default=False, verbose_name='بالکن')
    room = models.IntegerField(null=True, blank=True, verbose_name='اتاق')

    TypeEstate = models.ForeignKey(
        TypeEstateModel, on_delete=models.CASCADE, verbose_name='نوع ملک')

    created = models.DateField(
        default=timezone.now())

    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول املاک'
        verbose_name_plural = 'محصولات املاک'


class ImageEstateProductsModel(models.Model):
    products = models.ForeignKey(ProductsEstateModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ImageEstateProducts')

    def __str__(self):
        return self.products.name

    class Meta:
        verbose_name = 'تصاویر محصولات املاک'
        verbose_name_plural = 'تصاویر محصولات املاک'
