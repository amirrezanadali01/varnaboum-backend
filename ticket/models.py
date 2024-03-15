from dataclasses import dataclass
from operator import mod
from django.db import models
from django.contrib.auth.models import User

from office.models import OfficeModel, UserOfficeModel

ask = (
    ("complaint", "شکایت"),
    ("criticism", "شکایت و پیشنهاد"),

)


# Create your models here.
class TicketModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='سازنده')
    typeask = models.CharField(
        max_length=100, choices=ask, verbose_name='نوع تیکت')

    personal = models.ForeignKey(
        UserOfficeModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کارکن اداره')

    date = models.DateTimeField(auto_now_add=True, blank=True)

    office = models.ForeignKey(
        OfficeModel, on_delete=models.CASCADE, null=True, verbose_name='اداره')

    isfinish = models.BooleanField(default=False,  verbose_name='تموم شده')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class MessageTicketModel(models.Model):
    ticket = models.ForeignKey(
        TicketModel, on_delete=models.CASCADE, verbose_name='تیکت')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='فرستنده')
    text = models.TextField(null=True, verbose_name='متن')
    image = models.ImageField(
        upload_to='ImageTicket', null=True, blank=True, verbose_name='تصویر')
    video = models.FileField(
        upload_to='VideoTicket', null=True, blank=True, verbose_name='ویدیو')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    isread = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
