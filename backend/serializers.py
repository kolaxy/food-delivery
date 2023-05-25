from rest_framework import serializers
from .models import Restaurant, Dish, Order, OrderDetail
from django.core import serializers as sss


class DetailRestaurantSerializer(serializers.ModelSerializer):
    orders = serializers.JSONField(source='model_method')

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = (
            'model_method_field',
        )


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
