from django.db import models
from django.utils import timezone

from infousers.models import InfoUserModel

# Create your models here.
SOCIAL_MEDIA = (
    ("bycecle", "دوچرخه"),
    ("motorcycle", "موتور"),
    ("car", "ماشین"),

)


class TypeTransportationModel(models.Model):
    TypeTransportation = models.CharField(
        max_length=100, choices=SOCIAL_MEDIA, verbose_name='زیر مجموعه')
    name = models.CharField(max_length=100, verbose_name='نام')

    class Meta:
        verbose_name = 'زیر مجموعه محصولات حمل و نقل1'
        verbose_name_plural = 'زیر مجموعه محصولات حمل و نقل1'

    def __str__(self):
        return "{0} , {1}".format(self.TypeTransportation, self.name)


class SubTypeTransportationModel(models.Model):
    TypeTransportation = models.ForeignKey(
        TypeTransportationModel, on_delete=models.CASCADE, verbose_name='زیر مجموعه')
    name = models.CharField(max_length=100, verbose_name='نام')

    class Meta:
        verbose_name = 'زیر مجموعه محصولات حمل و نقل2'
        verbose_name_plural = 'زیر مجموعه محصولات حمل و نقل2'

    def __str__(self):
        return "{0} , {1}".format(self.TypeTransportation, self.name)


class ProductsTransportationModel(models.Model):
    infouser = models.ForeignKey(
        InfoUserModel, on_delete=models.CASCADE, verbose_name='صنف')
    image = models.ImageField(
        upload_to='ImageTransportationPreview', verbose_name='تصویر')
    name = models.CharField(max_length=300, verbose_name='نام')

    TypeTransportation = models.ForeignKey(
        TypeTransportationModel, on_delete=models.CASCADE,  verbose_name='زیرمجموعه1')
    SubTypeTransportation = models.ForeignKey(
        SubTypeTransportationModel, on_delete=models.CASCADE,  verbose_name='زیرمجموعه2')

    used = models.BigIntegerField(null=True,  verbose_name='کارکرده')
    price = models.BigIntegerField(verbose_name='قیمت')
    description = models.TextField(null=True,  verbose_name='توضیحات')

    created = models.DateField(
        default=timezone.now())

    time = models.TimeField(default=timezone.now)

    class Meta:
        verbose_name = 'محصولات حمل و نقل'
        verbose_name_plural = 'محصولات حمل و نقل'

    def __str__(self):
        return self.name


class ImageTransportationroductsModel(models.Model):
    products = models.ForeignKey(
        ProductsTransportationModel, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(
        upload_to='ImageTransportatioProducts', verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصاویر محصولات حمل و نقل'
        verbose_name_plural = 'تصاویر محصولات حمل و نقل'

    def __str__(self):
        return self.products.name
