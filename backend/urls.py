from django.urls import path, re_path, include
from backend.views import (
    RestaurantAPIList,
    RestaurantAPIUpdate,
    RestaurantAPIDestroy,
    DishAPIList,
    DishAPIUpdate,
    DishAPIDestroy,
    OrderAPIList,
    OrderAPIUpdate,
    OrderAPIDestroy,
    OrderDetailAPIList,
    OrderDetailAPIUpdate,
    OrderDetailAPIDestroy
)

urlpatterns = [
    path("v1/restaurant/", RestaurantAPIList.as_view()),
    path("v1/restaurant/<int:pk>/", RestaurantAPIUpdate.as_view()),
    path("v1/restaurant/<int:pk>/", RestaurantAPIDestroy.as_view()),
    path("v1/dish/", DishAPIList.as_view()),
    path("v1/dish/<int:pk>/", DishAPIUpdate.as_view()),
    path("v1/dish/<int:pk>/", DishAPIDestroy.as_view()),
    path("v1/order/", OrderAPIList.as_view()),
    path("v1/order/<int:pk>/", OrderAPIUpdate.as_view()),
    path("v1/order/<int:pk>/", OrderAPIDestroy.as_view()),
    path("v1/orderdetail/", OrderDetailAPIList.as_view()),
    path("v1/orderdetail/<int:pk>/", OrderDetailAPIUpdate.as_view()),
    path("v1/orderdetail/<int:pk>/", OrderDetailAPIDestroy.as_view()),

]
