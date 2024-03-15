from django.db import models
from django.contrib.auth.models import User
from infousers.models import InfoUserModel

# Create your models here.


class ViolationModel(models.Model):
    infouser = models.ForeignKey(
        InfoUserModel, on_delete=models.CASCADE, verbose_name='صنف')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    text = models.TextField(verbose_name='متن')

    def __str__(self):
        return self.infouser.name

    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = 'گزارش ها'
