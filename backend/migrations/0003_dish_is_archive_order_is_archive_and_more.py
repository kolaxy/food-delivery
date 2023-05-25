# Generated by Django 4.2.1 on 2023-05-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_orderdetail_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]
