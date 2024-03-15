from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CityModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'


class CategoryModel(models.Model):
    name = models.CharField(max_length=13, verbose_name='نام')
    icon = models.ImageField(upload_to='category')
    top = models.IntegerField(default=0, verbose_name='rank')
    isProducts = models.BooleanField(default=False)
    isPrice = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class SubCategoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return "{0} , {1}".format(self.category, self.name)

    class Meta:
        verbose_name = 'زیر مجوعه 1'
        verbose_name_plural = 'زیر مجموعه 1'


class SubtitleModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    subcategory = models.ForeignKey(
        SubCategoryModel, on_delete=models.CASCADE, verbose_name='زیرمجموعه 1')

    def __str__(self):
        return "{0} , {1}".format(self.subcategory, self.name)

    class Meta:
        verbose_name = 'زیر مجوعه 2'
        verbose_name_plural = 'زیر مجموعه 2'


# UPDATEEEEEEEEEEEEEEE

class VillageModel(models.Model):
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')
    name = models.CharField(max_length=200, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'روستا'
        verbose_name_plural = 'روستا ها'


class RegionCityModel(models.Model):
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')

    name = models.CharField(max_length=200, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'منطقه شهر'
        verbose_name_plural = 'منطقه شهر'
