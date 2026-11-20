from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserCreateAPIView(CreateAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer
#
#
# class UserListAPIView(ListAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer
#
#
# class UserUpdateAPIView(UpdateAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer
#
#
# class UserDestroyAPIView(DestroyAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer
#
#
# class UserRetrieveAPIView(RetrieveAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer
