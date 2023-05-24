from django.contrib import admin
from .models import Restaurant, Dish, Order, OrderDetail

admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderDetail)
