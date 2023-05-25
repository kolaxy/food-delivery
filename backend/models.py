from django.contrib.auth.models import User
from django.db import models
import json
from django.core.serializers.json import DjangoJSONEncoder


class Restaurant(models.Model):
    name = models.CharField(max_length=25)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def model_method(self):
        return Order.objects.filter(restaurant=self.pk).values()


class Dish(models.Model):
    name = models.CharField(max_length=25)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=25)
    phone = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return f'Order №{self.pk}'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return f'OrderDetail №{self.pk}/'
