from datetime import datetime
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from categories.models import CityModel
from office.models import OfficeModel, UserOfficeModel

# Create your models here.


class CategoryNewsModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='خبر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته بندی خبر'
        verbose_name_plural = 'دسته بندی اخبار'


class NewsPeopleModel(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    name = models.CharField(max_length=500, null=True,
                            blank=True, verbose_name='نام')
    titr = models.CharField(max_length=500, verbose_name='تیتر')
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')
    text = models.TextField(verbose_name='متن')
    image = models.ImageField(upload_to='NewsPeople', verbose_name='تصویر')
    video = models.FileField(
        upload_to='TrailerNewsPeople', null=True, blank=True, verbose_name='ویدیو')

    date_time = models.DateTimeField(default=datetime.now(), blank=True)

    submit = models.BooleanField(default=False, verbose_name='تایید')
    top = models.IntegerField(default=0, verbose_name='اولویت')

    def __str__(self):
        return self.titr

    class Meta:
        verbose_name = 'اخبار مردم'
        verbose_name_plural = 'اخبار مردم'


class NewsModel(models.Model):
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')

    user = models.ForeignKey(
        UserOfficeModel, on_delete=models.CASCADE, verbose_name='کاربر')
    office = models.ForeignKey(
        OfficeModel, on_delete=models.CASCADE, verbose_name='اداره')

    titr = models.CharField(max_length=500, verbose_name='تیتر')
    text = models.TextField(verbose_name='متن')
    image = models.ImageField(upload_to='News', verbose_name='تصویر')
    video = models.FileField(
        upload_to='TrailerNewsOffice', null=True, blank=True, verbose_name='تیزر')

    category = models.ForeignKey(
        CategoryNewsModel, on_delete=models.CASCADE, verbose_name='دسته بندی')

    date_time = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.titr

    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'


class TopNewsModel(models.Model):
    office = models.OneToOneField(
        OfficeModel, on_delete=models.CASCADE, verbose_name='اداره')

    def __str__(self):
        return self.office.name

    class Meta:
        verbose_name = 'اخبار برتر'
        verbose_name_plural = 'اخبار برتر'
