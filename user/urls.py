from django.urls import path
from rest_framework.routers import DefaultRouter

from user.apps import UsersConfig
from user.views import UserViewSet

# from users.views import (UserCreateAPIView, UserListAPIView, UserUpdateAPIView,
#                          UserDestroyAPIView, UserRetrieveAPIView, UserViewSet)

app_name = UsersConfig.name
router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    # path("users/", UserListAPIView.as_view(), name="user_list"),
    # path("users/create/", UserCreateAPIView.as_view(), name="user_create"),
    # path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    # path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    # path("users/<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="users_destroy"),
] + router.urls
