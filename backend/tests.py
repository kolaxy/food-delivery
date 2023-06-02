from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from backend.models import Restaurant, Order, OrderDetail, Dish
from django.contrib.auth.models import User, Group
from .serializers import *


class SetItUp(APITestCase):
    """Setup class for test db"""

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser', password='superuser')
        self.restaurateur1 = User.objects.create_user(username='restaurateur1', password='restaurateur1')
        self.restaurateur2 = User.objects.create_user(username='restaurateur2', password='restaurateur2')
        self.customer1 = User.objects.create_user(username='customer1', password='customer1')
        self.customer2 = User.objects.create_user(username='customer2', password='customer2')
        self.restorators = Group.objects.filter(name='restorators').first()
        self.customers = Group.objects.filter(name='customers').first()

        self.restaurateur1.groups.add(self.restorators)
        self.restaurateur2.groups.add(self.restorators)
        self.customer1.groups.add(self.customers)
        self.customer2.groups.add(self.customers)
        self.superuser.save()
        self.restaurateur1.save()
        self.restaurateur2.save()
        self.customer1.save()
        self.customer2.save()

        self.restaurant1 = Restaurant.objects.create(name='restaurant1', restaurateur=self.restaurateur1)
        self.restaurant2 = Restaurant.objects.create(name='restaurant1', restaurateur=self.restaurateur2)
        self.restaurant1.save()
        self.restaurant2.save()

        self.dish1_1 = Dish.objects.create(name='dish1_1', restaurant=self.restaurant1)
        self.dish1_2 = Dish.objects.create(name='dish1_2', restaurant=self.restaurant1)
        self.dish2_1 = Dish.objects.create(name='dish2_1', restaurant=self.restaurant2)
        self.dish2_2 = Dish.objects.create(name='dish2_2', restaurant=self.restaurant2)

        self.dish1_1.save()
        self.dish1_2.save()
        self.dish2_1.save()
        self.dish2_2.save()

        self.order1 = Order.objects.create(customer=self.customer1, address='address1', phone=1,
                                           restaurant=self.restaurant1)
        self.order2 = Order.objects.create(customer=self.customer2, address='address2', phone=2,
                                           restaurant=self.restaurant2)

        self.order1.save()
        self.order2.save()

        self.orderdetail1 = OrderDetail.objects.create(order=self.order1, dish=self.dish1_1, price=1, quantity=1)
        self.orderdetail2 = OrderDetail.objects.create(order=self.order2, dish=self.dish2_1, price=2, quantity=2)

        self.orderdetail1.save()
        self.orderdetail2.save()

        self.superuser_token = Token.objects.create(user=self.superuser)
        self.restaurateur1_token = Token.objects.create(user=self.restaurateur1)
        self.restaurateur2_token = Token.objects.create(user=self.restaurateur2)
        self.customer1_token = Token.objects.create(user=self.customer1)
        self.customer2_token = Token.objects.create(user=self.customer2)


class RestTests(SetItUp):

    def test_restaurant(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('restaurant'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.post(reverse('restaurant'),
                                    data={'name': 'resttest1', 'restaurateur': self.restaurateur1.id})
        self.assertEqual(response.status_code, 201)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('restaurant'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('restaurant'),
                                    data={'name': 'resttest2', 'restaurateur': self.restaurateur2.id})
        self.assertEqual(response.status_code, 201)

        # customer auth

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('restaurant'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('restaurant'),
                                    data={'name': 'resttest3', 'restaurateur': self.customer1.id})
        self.assertEqual(response.status_code, 403)

    def test_restaurant_detail(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('restaurant_detail', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('restaurant_detail', kwargs={'pk': self.restaurant1.id}),
                                   data={'name': 'resttest2', 'restaurateur': self.restaurateur1.id})
        self.assertEqual(response.status_code, 200)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('restaurant_detail', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 200)

        # response = self.client.put(reverse('restaurant_detail', kwargs={'pk': self.restaurant1.id}),
        #                            data={'name': 'resttest2', 'restaurateur': self.restaurateur1.id})
        # self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('restaurant_detail', kwargs={'pk': self.restaurant2.id}))
        self.assertEqual(response.status_code, 200)

        # customer auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('restaurant_detail', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('restaurant_detail', kwargs={'pk': self.restaurant1.id}),
                                   data={'name': 'resttest2', 'restaurateur': self.restaurateur1.id})
        self.assertEqual(response.status_code, 403)

    def test_restaurantorders(self):
        # auth
        response = self.client.get(reverse('restaurant_orders_filter', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 401)

        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('restaurant_orders_filter', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 200)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('restaurant_orders_filter', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 200)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('restaurant_orders_filter', kwargs={'pk': self.restaurant2.id}))
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('restaurant_orders_filter', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 403)

    def test_restaurantdelete(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.delete(reverse('restaurant_delete', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 204)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.delete(reverse('restaurant_delete', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur2_token.key)
        response = self.client.delete(reverse('restaurant_delete', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.delete(reverse('restaurant_delete', kwargs={'pk': self.restaurant1.id}))
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.delete(reverse('restaurant_delete', kwargs={'pk': self.restaurateur2.id}))
        self.assertEqual(response.status_code, 403)


class DishTests(SetItUp):

    def test_dish(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('dish'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('dish'), data={'name': 'dish1', 'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 201)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('dish'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('dish'), data={'name': 'dish1', 'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('dish'), data={'name': 'dish1', 'restaurant': self.restaurant2.id})
        self.assertEqual(response.status_code, 403)

        # cust auth

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('dish'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('dish'), data={'name': 'dish1', 'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse('dish'), data={'name': 'dish1', 'restaurant': self.restaurant2.id})
        self.assertEqual(response.status_code, 403)

    def test_dish_detail(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}),
                                   data={'name': 'dish_su', 'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('dish_detail', kwargs={'pk': self.dish2_1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}),
                                   data={'name': 'dish_su', 'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)

        # response = self.client.put(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}),
        #                            data={'name': 'dish_su', 'restaurant': self.restaurant2.id})
        # self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('dish_detail', kwargs={'pk': self.dish1_1.id}),
                                   data={'name': 'dish_su', 'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 403)

    def test_dish_delete(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.delete(reverse('dish_delete', kwargs={'pk': self.dish1_2.id}))
        self.assertEqual(response.status_code, 204)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.delete(reverse('dish_delete', kwargs={'pk': self.dish1_1.id}))
        self.assertEqual(response.status_code, 204)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.delete(reverse('dish_delete', kwargs={'pk': self.dish2_1.id}))
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.delete(reverse('dish_delete', kwargs={'pk': self.dish1_1.id}))
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer2_token.key)
        response = self.client.delete(reverse('dish_delete', kwargs={'pk': self.dish2_1.id}))
        self.assertEqual(response.status_code, 403)


class OrderTests(SetItUp):
    def test_order(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('order'),
                                    data={'customer': self.superuser.id, 'address': 'add1', 'phone': 123,
                                          'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 201)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('order'),
                                    data={'customer': self.superuser.id, 'address': 'add1', 'phone': 123,
                                          'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 201)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('order'),
                                    data={'customer': self.superuser.id, 'address': 'add1', 'phone': 123,
                                          'restaurant': self.restaurant1.id})
        self.assertEqual(response.status_code, 201)

    def test_order_detail(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('order_detail', kwargs={'pk': self.order1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('order_detail', kwargs={'pk': self.order1.id}),
                                   data={'address': 'yoyo1337', 'restaurant': self.restaurant1.id,
                                         'customer': self.customer1.id, 'phone': 1337})
        self.assertEqual(response.status_code, 200)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('order_detail', kwargs={'pk': self.order1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('order_detail', kwargs={'pk': self.order1.id}),
                                   data={'address': 'yoyo1337', 'restaurant': self.restaurant1.id,
                                         'customer': self.customer1.id, 'phone': 1337})
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('order_detail', kwargs={'pk': self.order1.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.put(reverse('order_detail', kwargs={'pk': self.order1.id}),
                                   data={'address': 'yoyo1337', 'restaurant': self.restaurant1.id,
                                         'customer': self.customer1.id, 'phone': 1337})
        self.assertEqual(response.status_code, 403)

    def test_dish_delete(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.delete(reverse('order_delete', kwargs={'pk': self.order1.id}))
        self.assertEqual(response.status_code, 204)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.delete(reverse('order_delete', kwargs={'pk': self.order1.id}))
        self.assertEqual(response.status_code, 204)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.delete(reverse('order_delete', kwargs={'pk': self.order2.id}))
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.delete(reverse('order_delete', kwargs={'pk': self.order1.id}))
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer2_token.key)
        response = self.client.delete(reverse('order_delete', kwargs={'pk': self.order2.id}))
        self.assertEqual(response.status_code, 403)


class OrderDetailTest(SetItUp):

    def test_orderdetail(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('orderdetail'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('orderdetail'),
                                    data={'order': self.order1.id, 'dish': self.dish1_1.id, 'quantity': 20,
                                          'price': 50})
        self.assertEqual(response.status_code, 201)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('orderdetail'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('orderdetail'),
                                    data={'order': self.order1.id, 'dish': self.dish1_1.id, 'quantity': 20,
                                          'price': 50})
        self.assertEqual(response.status_code, 201)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('orderdetail'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('orderdetail'),
                                    data={'order': self.order1.id, 'dish': self.dish1_1.id, 'quantity': 20,
                                          'price': 50})
        self.assertEqual(response.status_code, 201)

    def test_orderdetail_detail(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail1.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail1.id}),
                                   data={'order': self.order1.id, 'dish': self.dish1_1.id, 'quantity': 100,
                                         'price': 50})
        self.assertEqual(response.status_code, 200)
    #
        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.get(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail1.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.put(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail1.id}),
                                   data={'order': self.order1.id, 'dish': self.dish1_1.id, 'quantity': 123,
                                         'price': 50})
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.get(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.put(reverse('orderdetail_detail', kwargs={'pk': self.orderdetail1.id}),
                                   data={'order': self.order1.id, 'dish': self.dish1_1.id, 'quantity': 123,
                                         'price': 50})
        self.assertEqual(response.status_code, 403)

    def test_orderdetaildelete(self):
        # su auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.delete(reverse('orderdetail_delete', kwargs={'pk': self.orderdetail1.id}))
        self.assertEqual(response.status_code, 204)

        # rest auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.restaurateur1_token.key)
        response = self.client.delete(reverse('orderdetail_delete', kwargs={'pk': self.orderdetail1.id}))
        self.assertEqual(response.status_code, 403)

        # cust auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        response = self.client.delete(reverse('orderdetail_delete', kwargs={'pk': self.orderdetail1.id}))
        self.assertEqual(response.status_code, 403)
