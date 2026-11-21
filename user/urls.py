from django.db import router
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.apps import UsersConfig
from user.views import PaymentListAPIView, UserCreateAPIView

from user.views import (UserCreateAPIView, UserListAPIView, UserUpdateAPIView,
                         UserDestroyAPIView, UserRetrieveAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name='payments_list'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("", UserListAPIView.as_view(), name="user_list"),
    path("create/", UserCreateAPIView.as_view(), name="user_create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="user_destroy"),
]
