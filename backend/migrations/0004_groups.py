# Generated by Django 4.2.1 on 2023-05-26 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    user = User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )


def add_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'restorators'),
        Group(name=u'customers'),
    ])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0003_remove_dish_restaurateur_restaurant_restaurateur'),
    ]

    operations = [
        migrations.RunPython(add_groups),
        migrations.RunPython(create_superuser),
    ]
