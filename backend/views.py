from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant, Dish, Order, OrderDetail
from rest_framework import generics
from .serializers import RestaurantSerializer, DishSerializer, OrderSerializer, OrderDetailSerializer


def home(request):
    return HttpResponse('<h1>FOOD DELIVERY</h1>')


class RestaurantAPIList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class DishAPIList(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderAPIList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailAPIList(generics.ListCreateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class OrderDetailAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class OrderDetailAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
