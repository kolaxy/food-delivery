# Generated by Django 4.2.1 on 2023-05-26 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0002_dish_restaurateur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='restaurateur',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='restaurateur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
