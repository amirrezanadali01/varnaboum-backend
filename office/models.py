from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from categories.models import CityModel

# Create your models here.


class OfficeModel(models.Model):
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')
    name = models.CharField(max_length=200, verbose_name='نام')
    address = models.CharField(max_length=500, verbose_name='ادرس')
    bio = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    instagram = models.CharField(max_length=200, blank=True, null=True)
    profile = models.ImageField(
        upload_to='ProfileOffice', verbose_name='پروفایل')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)
    video = models.FileField(
        upload_to='TrailerOffice', null=True, blank=True, verbose_name='تیزر')

    number = models.BigIntegerField(
        null=True, blank=True, verbose_name='شماره تماس')

    preview = models.ImageField(
        upload_to='PreviewOffice', verbose_name='عکس نمایه')
    icon = models.ImageField(upload_to='IconOffice', verbose_name='ایکون')
    top = models.IntegerField(default=0, verbose_name='اولویت')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'اداره'
        verbose_name_plural = 'ادارات'


class UserOfficeModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    office = models.ForeignKey(
        OfficeModel, on_delete=models.CASCADE, verbose_name='اداره ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'افراد ادره'
        verbose_name_plural = 'افراد اداره'
