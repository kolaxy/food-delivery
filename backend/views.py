import logging

from django.shortcuts import render, get_object_or_404
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
import logging

logger = logging.getLogger('main')


def home(request):
    logger.info('HOME')
    return HttpResponse('<h1>FOOD DELIVERY</h1>')


class RestaurantAPIList(generics.ListCreateAPIView):
    """Restaurants list ( ALL ) + CREATE ( SUPERUSER + USER.GROUPS REST )"""
    queryset = Restaurant.objects.filter(is_archive=False)
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        if 'restorators' in [i.name for i in self.request.user.groups.all()] or self.request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            logger.info(f'RestaurantAPIList -- {serializer.errors}')
            serializer.is_valid(raise_exception=True)
        logger.info(f'RestaurantAPIList -- permission denied')
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
        logger.info(f'RestaurantOrdersAPIList -- permission denied')
        raise PermissionDenied


class RestaurantAPIUpdate(generics.RetrieveUpdateAPIView):
    """Restaurant info update ( ADMIN + RESTAURANT USER BY ID )"""
    queryset = Restaurant.objects.filter(is_archive=False)
    serializer_class = RestaurantSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            if (self.request.user.id == Restaurant.objects.get(pk=instance.pk).restaurateur.id and request.data[
                'restaurateur'] == Restaurant.objects.get(
                pk=instance.pk).restaurateur.id) or self.request.user.is_staff:
                self.perform_update(serializer)
                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            else:
                logger.info(
                    f'RestaurantAPIUpdate -- instance : {instance} , request : {request.data}. ID does not match')
        else:
            logger.info(f'RestaurantAPIList -- {serializer.errors}')
            serializer.is_valid(raise_exception=True)
        logger.info(f'RestaurantAPIUpdate -- permission denied')
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
        if serializer.is_valid(raise_exception=False):
            if Restaurant.objects.get(
                    pk=self.request.data[
                        'restaurant']).restaurateur.id == self.request.user.id or self.request.user.is_staff:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        serializer.is_valid(raise_exception=True)
        logger.info(
            f'ListCreateAPIView -- permission denied. restaurateur id = {Restaurant.objects.get(pk=self.request.data["restaurant"]).restaurateur.id}, user id = {self.request.user.id} ')
        raise PermissionDenied


class DishAPIUpdate(generics.RetrieveUpdateAPIView):
    """Dish update ( ADMIN + RESTAURANT USER )"""
    queryset = Dish.objects.filter(is_archive=False)
    serializer_class = DishSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            if (instance.restaurant.id == int(request.data['restaurant']) and User.objects.get(
                    pk=Restaurant.objects.get(
                        pk=instance.restaurant.id).restaurateur.id).id == self.request.user.id) or self.request.user.is_staff:
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
                return Response(serializer.data)
            logger.info(f'DishAPIUpdate -- CHECK permissions and entered data : {request.data}, {self.request.user.id}')
        else:
            logger.info(f'DishAPIUpdate -- {serializer.errors}')
        raise PermissionDenied


class DishAPIDestroy(generics.RetrieveDestroyAPIView):
    """Dish delete ( ADMIN + RESTAURANT USER )"""
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff or ('restorators' in [i.name for i in
                                                            self.request.user.groups.all()] and instance.restaurant.id == Restaurant.objects.get(
            restaurateur=self.request.user.id).id):
            instance.is_archive = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        logger.info(f'DishAPIUpdate -- permission denied')
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

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        if self.request.user.id in (
                obj.customer, User.objects.get(pk=obj.restaurant.restaurateur.id).id) or self.request.user.is_staff:
            return obj
        logger.info(
            f'OrderAPIUpdate -- get_object -- user id {self.request.user.id} , object customer , restaurateur : {obj.customer, User.objects.get(pk=obj.restaurant.restaurateur.id).id} ')
        raise PermissionDenied

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.request.user.is_staff:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        logger.info(f'User is not admin ( id = {self.request.user.id}')
        raise PermissionDenied


class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    """Order delete ( YES to restaurant by RESTAURANT ID, YES FOR ADMIN )"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff or ('restorators' in [i.name for i in
                                                            self.request.user.groups.all()] and instance.restaurant == Restaurant.objects.get(
            restaurateur=self.request.user)):
            instance.is_archive = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        logger.info(f'OrderAPIDestroy -- permission denied. user id : {self.request.user.id}')
        raise PermissionDenied


class OrderDetailAPIList(generics.ListCreateAPIView):
    """OrderDetail create ( YES to user BY USER ID, YES to restaurant BY RESTAURANT ID, YES for ADMIN )"""
    queryset = OrderDetail.objects.filter(is_archive=False)
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            if Order.objects.get(pk=self.request.data['order']).restaurant == Dish.objects.get(
                    pk=self.request.data['dish']).restaurant:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                logger.info(
                    f'''DishAPIUpdate -- You tried to create item with Restaurant id {Order.objects.get(pk=self.request.data['order']).restaurant}
                while it is {Dish.objects.get(
                        pk=self.request.data['dish']).restaurant}''')
        else:
            logger.info(f'DishAPIUpdate -- {serializer.errors}')
            serializer.is_valid(raise_exception=True)
        return Response({"detail": "Input is not valid"}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIUpdate(generics.RetrieveUpdateAPIView):
    """OrderDetail update, ( ADMIN ONLY !)"""
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    # permission_classes = (IsAdminUser,)
    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        try:
            if self.request.user.is_staff or self.request.user.id == (
                    Restaurant.objects.get(pk=(Dish.objects.get(pk=self.kwargs['pk']).restaurant).id)).restaurateur.id:
                return obj
            raise PermissionDenied
        except:
            raise PermissionDenied

    def update(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=False):
                self.perform_update(serializer)
                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
                return Response(serializer.data)
            # serializer.is_valid(raise_exception=False)
            logger.info(f'OrderDetailAPIUpdate --{serializer.errors}')
            serializer.is_valid(raise_exception=True)
        logger.info(f'OrderDetailAPIUpdate -- ID {self.request.user.id}. Not admin to update.')
        raise PermissionDenied


class OrderDetailAPIDestroy(generics.RetrieveDestroyAPIView):
    """OrderDetail update, ( ADMIN ONLY !)"""
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archive = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
