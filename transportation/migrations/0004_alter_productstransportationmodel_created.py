# Generated by Django 4.0.3 on 2023-01-12 12:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0003_alter_productstransportationmodel_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstransportationmodel',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 12, 32, 48, 435587, tzinfo=utc)),
        ),
    ]
