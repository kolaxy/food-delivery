from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant, Dish, Order, OrderDetail
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly
from .serializers import RestaurantSerializer, DishSerializer, OrderSerializer, OrderDetailSerializer, \
    DetailRestaurantSerializer
from rest_framework import status
from backend.models import Restaurant, Order, OrderDetail, Dish
from rest_framework.permissions import *
from django.http import HttpResponseForbidden
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User


def home(request):
    return HttpResponse('<h1>FOOD DELIVERY</h1>')


class RestaurantAPIList(generics.ListCreateAPIView):
    """Restaurants list ( ALL ) + CREATE ( SUPERUSER + USER.GROUPS REST )"""
    queryset = Restaurant.objects.filter(is_archive=False)
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        if 'restorators' in [i.name for i in self.request.user.groups.all()] or self.request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        raise PermissionDenied


class RestaurantOrdersAPIList(generics.ListAPIView):
    """Restaurant menu ( + DISH objects) ( ALL )"""
    queryset = Restaurant.objects.filter(is_archive=False)
    serializer_class = DetailRestaurantSerializer

    def get_queryset(self):
        if 'restorators' in [i.name for i in self.request.user.groups.all()] or self.request.user.is_staff:
            if self.request.user.is_staff:
                return Restaurant.objects.filter(pk=self.kwargs['pk'], is_archive=False)
            if Restaurant.objects.filter(pk=self.kwargs['pk'],
                                         is_archive=False).first().restaurateur.id == self.request.user.id:
                return Restaurant.objects.filter(pk=self.kwargs['pk'], is_archive=False)
        raise PermissionDenied


class RestaurantAPIUpdate(generics.RetrieveUpdateAPIView):
    """Restaurant info update ( ADMIN + RESTAURANT USER BY ID )"""
    queryset = Restaurant.objects.filter(is_archive=False)
    serializer_class = RestaurantSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if (self.request.user.id == Restaurant.objects.get(pk=instance.pk).restaurateur.id and request.data[
            'restaurateur'] == Restaurant.objects.get(pk=instance.pk).restaurateur.id) or self.request.user.is_staff:
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        raise PermissionDenied


class RestaurantAPIDestroy(generics.RetrieveDestroyAPIView):
    """Restaurant delete ( ADMIN )"""
    queryset = Restaurant.objects.filter(is_archive=False)
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archive = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DishAPIList(generics.ListCreateAPIView):
    """Dish list + detail, ( ALL )"""
    queryset = Dish.objects.filter(is_archive=False)
    serializer_class = DishSerializer

    def get_queryset(self):
        if self.request.query_params.get('restaurant', None):
            return Dish.objects.filter(restaurant=self.request.query_params['restaurant'], is_archive=False)
        return Dish.objects.filter(is_archive=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Restaurant.objects.get(
                pk=self.request.data['restaurant']).id == self.request.user.id or self.request.user.is_staff:
            # self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        raise PermissionDenied


class DishAPIUpdate(generics.RetrieveUpdateAPIView):
    """Dish update ( ADMIN + RESTAURANT USER )"""
    queryset = Dish.objects.filter(is_archive=False)
    serializer_class = DishSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.restaurant.id == request.data['restaurant'] and instance.restaurant.id == User.objects.get(
                pk=Restaurant.objects.get(pk=instance.restaurant.id).id).id or self.request.user.is_staff:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        raise PermissionDenied


class DishAPIDestroy(generics.RetrieveDestroyAPIView):
    """Dish delete ( ADMIN + RESTAURANT USER )"""
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.restaurant.id == request.data['restaurant'] and instance.restaurant.id == User.objects.get(
                pk=Restaurant.objects.get(pk=instance.restaurant.id).id).id or self.request.user.is_staff:
            instance.is_archive = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied


class OrderAPIList(generics.ListCreateAPIView):
    """Order lists ( user's BY USER ID, all restaurant id BY RESTAURANT ID, all for ADMIN )
    + BOOL FALSE with ?is_archive=1"""
    queryset = Order.objects.filter(is_archive=False)
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        elif 'restorators' in [i.name for i in self.request.user.groups.all()]:
            return Order.objects.filter(restaurant=Restaurant.objects.get(restaurateur=self.request.user.id),
                                        is_archive=False)
        return Order.objects.filter(customer=self.request.user.id)


class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    """Order detail ( + Dishes ), ( YES to user BY USER ID, YES to restaurant BY RESTAURANT ID, YES for ADMIN ) """
    queryset = Order.objects.filter(is_archive=False)
    serializer_class = OrderSerializer
    permission_classes = IsAdminUser

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     if instance.restaurant.id == request.data['restaurant'] and instance.restaurant.id == User.objects.get(
    #             pk=Restaurant.objects.get(pk=instance.restaurant.id).id).id or self.request.user.is_staff:
    #         serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #
    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             # If 'prefetch_related' has been applied to a queryset, we need to
    #             # forcibly invalidate the prefetch cache on the instance.
    #             instance._prefetched_objects_cache = {}
    #
    #         return Response(serializer.data)
    #     raise PermissionDenied
    # КТО ДОЛЖЕН ИЗМЕНЯТЬ? НИКТО. ТОЛЬКО АДМИН МОЖЕТ УДАЛЯТЬ == СТАВИТЬ БУЛЕВО ЗНАЧЕНИЕ IS ARCHIVE НА TRUE СНИЗУ


class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    """Order delete ( YES to restaurant by RESTAURANT ID, YES FOR ADMIN )"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.restaurant == Restaurant.objects.get(restaurateur=self.request.user) or self.request.user.is_staff:
            instance.is_archive = True
            # instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied


class OrderDetailAPIList(generics.ListCreateAPIView):
    """OrderDetail create ( YES to user BY USER ID, YES to restaurant BY RESTAURANT ID, YES for ADMIN )"""
    queryset = OrderDetail.objects.filter(is_archive=False)
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Order.objects.get(pk=self.request.data['order']).restaurant == Dish.objects.get(
                pk=self.request.data['dish']).restaurant:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"detail": "Input is not valid"}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIUpdate(generics.RetrieveUpdateAPIView):
    """OrderDetail update, ( ADMIN ONLY !)"""
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = IsAdminUser

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if Order.objects.get(pk=self.request.data['order']).restaurant == Dish.objects.get(
                pk=self.request.data['dish']).restaurant:
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({"detail": "Input data for editing is not valid"}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIDestroy(generics.RetrieveDestroyAPIView):
    """OrderDetail update, ( ADMIN ONLY !)"""
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = IsAdminUser

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archive = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
