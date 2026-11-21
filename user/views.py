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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import User, Payment
from user.permissions import IsOwnerOrReadOnly
from user.serializers import UserSerializer, PaymentSerializer, UserTokenObtainPairSerializer, UserPublicSerializer


# class UserTokenObtainPairView(TokenObtainPairView):
#     serializer_class = UserTokenObtainPairSerializer

# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()



class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserSerializer
        return UserPublicSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("payment_date",)
