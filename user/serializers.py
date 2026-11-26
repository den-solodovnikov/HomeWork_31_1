from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User, Payment, Subscribe


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["first_name"] = user.first_name
        token["lasst_name"] = user.last_name
        token["email"] = user.email

        return token


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source="payment_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_staff",
            "is_active",
            "is_superuser",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone",
            "city",
            "avatar",
            "payments",
        )


class UserPublicSerializer(serializers.ModelSerializer):
    """Публичный сериализатор для просмотра чужого профиля."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "phone",
            "city",
            "avatar",
        ]


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"
