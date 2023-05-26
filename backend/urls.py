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
    path("restaurant/", RestaurantAPIList.as_view()),
    path("restaurant/<int:pk>/", RestaurantAPIUpdate.as_view()),
    path("restaurantorders/<int:pk>/", RestaurantOrdersAPIList.as_view()),
    path("restaurantdelete/<int:pk>/", RestaurantAPIDestroy.as_view()),
    path("dish/", DishAPIList.as_view()),
    path("dish/<int:pk>/", DishAPIUpdate.as_view()),
    path("dishdelete/<int:pk>/", DishAPIDestroy.as_view()),
    path("order/", OrderAPIList.as_view()),
    path("order/<int:pk>/", OrderAPIUpdate.as_view()),
    path("orderdelete/<int:pk>/", OrderAPIDestroy.as_view()),
    path("orderdetail/", OrderDetailAPIList.as_view()),
    path("orderdetail/<int:pk>/", OrderDetailAPIUpdate.as_view()),
    path("orderdetaildelete/<int:pk>/", OrderDetailAPIDestroy.as_view()),


    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
]
