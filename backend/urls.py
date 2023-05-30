from django.urls import path, re_path, include
from backend.views import (
    # RestaurantList, RestaurantDetail
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
    OrderDetailAPIDestroy, RestaurantOrdersAPIList,
    # DetailRestaurantAPIList,

    # RestaurantViewSet
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

urlpatterns = [
    path("restaurant/", RestaurantAPIList.as_view(), name="restaurant"),
    path("restaurant/<int:pk>/", RestaurantAPIUpdate.as_view(), name="restaurant_detail"),
    path("restaurantorders/<int:pk>/", RestaurantOrdersAPIList.as_view(), name="restaurant_orders_filter"),
    path("restaurantdelete/<int:pk>/", RestaurantAPIDestroy.as_view(), name="restaurant_delete"),
    path("dish/", DishAPIList.as_view(), name="dish"),
    path("dish/<int:pk>/", DishAPIUpdate.as_view(), name="dish_detail"),
    path("dishdelete/<int:pk>/", DishAPIDestroy.as_view(), name="dish_delete"),
    path("order/", OrderAPIList.as_view(), name="order"),
    path("order/<int:pk>/", OrderAPIUpdate.as_view(), name="order_detail"),
    path("orderdelete/<int:pk>/", OrderAPIDestroy.as_view(), name="order_delete"),
    path("orderdetail/", OrderDetailAPIList.as_view(), name="orderdetail"),
    path("orderdetail/<int:pk>/", OrderDetailAPIUpdate.as_view(), name="orderdetail_detail"),
    path("orderdetaildelete/<int:pk>/", OrderDetailAPIDestroy.as_view(), name="orderdetail_delete"),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
]
