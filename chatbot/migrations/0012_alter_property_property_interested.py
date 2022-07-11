# Generated by Django 3.2.5 on 2022-07-11 20:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatbot', '0011_auto_20220711_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_interested',
            field=models.ManyToManyField(related_name='user_interested', to=settings.AUTH_USER_MODEL),
        ),
    ]
