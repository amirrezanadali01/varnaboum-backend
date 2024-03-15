from operator import mod
from statistics import mode
from time import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from categories.models import CategoryModel, RegionCityModel, SubCategoryModel, CityModel, SubtitleModel, VillageModel
from django.utils import timezone
# Create your models here.


class InfoUserModel(models.Model):
    city = models.ForeignKey(
        CityModel, on_delete=models.CASCADE, verbose_name='شهر')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    name = models.CharField(max_length=200, verbose_name='نام')
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, verbose_name='دسته بندی')
    subcategory = models.ManyToManyField(
        SubCategoryModel, null=True, blank=True, verbose_name='زیر مجموعه 1')
    subtitle = models.ManyToManyField(
        SubtitleModel, null=True, blank=True, verbose_name='زیر مجموعه 2')
    Confirmation = models.BooleanField(default=False, verbose_name='تایید')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)
    number = models.BigIntegerField(
        null=True, blank=True, verbose_name='شماره تماس')
    profile = models.ImageField(upload_to='Profile', blank=True, null=True)
    bio = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    instagram = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=500, verbose_name='ادرس')
    tags = models.TextField()
    video = models.FileField(
        upload_to='Trailer', null=True, blank=True, verbose_name='تیزر')
    top = models.IntegerField(default=0, verbose_name='rank')

    village = models.ForeignKey(
        VillageModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name='روستا')
    region = models.ForeignKey(
        RegionCityModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name='منطقه')

    class Meta:
        verbose_name = 'صنف'
        verbose_name_plural = 'اصناف'

    def __str__(self):
        return self.user.username


class VerifyCodeModel(models.Model):
    number = models.BigIntegerField()
    code = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    token = models.TextField(blank=True, null=True)
    valid = models.IntegerField(default=0)


class ContactUsModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)
    number = models.BigIntegerField(
        null=True, blank=True, verbose_name='شماره تماس')
    profile = models.ImageField(upload_to='Profile', blank=True, null=True)
    bio = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    instagram = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=500, verbose_name='ادرس')
    video = models.FileField(
        upload_to='Trailer', null=True, blank=True, verbose_name='تیزر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما'


class Shop_Image(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    imag = models.ImageField(upload_to='ShopImage',
                             blank=True, null=True, verbose_name='تصویر')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'تصویر صنف'
        verbose_name_plural = 'تصاویر اصناف'


class QuestionProfileModel(models.Model):
    question = models.TextField(verbose_name='سوال')
    is_required = models.BooleanField(default=False, verbose_name='اجباری')
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'سوالات صنف'
        verbose_name_plural = 'سوالات اصناف'

    def __str__(self):
        return self.question


class AnswerProfileModel(models.Model):
    answer = models.TextField(verbose_name='پاسخ')
    question = models.ForeignKey(
        QuestionProfileModel, on_delete=models.CASCADE, verbose_name='سوال')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')

    class Meta:
        verbose_name = 'پاسخ سوال'
        verbose_name_plural = 'پاسخ سوالات'

    def __str__(self):
        return self.user.username


class ProductsAnotherModel(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام')
    preview = models.ImageField(
        upload_to='ProductsPreviewAnother')
    description = models.TextField(
        null=True, blank=True, verbose_name='توضیحات')
    infouser = models.ForeignKey(
        InfoUserModel, on_delete=models.CASCADE, verbose_name='صنف')
    price = models.BigIntegerField(null=True, verbose_name='قیمت')

    created = models.DateField(
        default=timezone.now())

    time = models.TimeField(default=timezone.now)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name


class ProductsImageAnotherModel(models.Model):
    products = models.ForeignKey(
        ProductsAnotherModel, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(
        upload_to='ProductsPreviewAnotherImage', verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'

    def __str__(self):
        return self.products.name


class ManagerStore(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    category = models.ManyToManyField(
        CategoryModel, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'مدیریت صنف'
        verbose_name_plural = 'مدیریت اصناف'

    def __str__(self):
        return self.name
