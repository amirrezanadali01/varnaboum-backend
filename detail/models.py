from django.db import models

# Create your models here.

SOCIAL_MEDIA = (
    ("instagram", "instagram"),
    ("site", "site"),
    ("phone", "phone"),
    ("varnaboom", "varnaboom"),

)


class Banner(models.Model):
    image = models.ImageField(upload_to='banner', verbose_name='تصویر')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    action = models.CharField(
        max_length=100, choices=SOCIAL_MEDIA, verbose_name='رویداد')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'


class UpdateVersionModel(models.Model):
    version = models.IntegerField()

    def __str__(self):
        return str(self.version)
