from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.viewsets import ModelViewSet

from user.models import User, Payment
from user.serializers import UserSerializer, PaymentSerializer


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


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("payment_date",)
