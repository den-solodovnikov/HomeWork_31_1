from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lessons.models import Course
from user.models import User, Payment, Subscribe
from user.permissions import IsOwnerOrReadOnly
from user.serializers import (
    UserSerializer,
    PaymentSerializer,
    UserPublicSerializer,
)
from user.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    retrieve_stripe_session,
)


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


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course = payment.course

        # Создаем продукт, цену и сессию в Stripe
        product = create_stripe_product(course.title)
        price = create_stripe_price(course.price, product)
        session_id, payment_link = create_stripe_session(price)

        # Сохраняем ID сессии и ссылку в созданный объект платежа
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("payment_dateList",)


class PaymentStatusAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Проверка статуса платежа в Stripe",
        operation_description="Запрашивает актуальный статус сессии оплаты в Stripe по ID платежа в базе данных.",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID платежа в системе",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Статус платежа успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "payment_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=15
                        ),
                        "session_id": openapi.Schema(
                            type=openapi.TYPE_STRING, example="cs_test_a0htQSL..."
                        ),
                        "payment_status": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "payment_status": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="paid"
                                ),
                                "status": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="complete"
                                ),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="У платежа отсутствует session_id Stripe"
            ),
            401: openapi.Response(description="Пользователь не авторизован"),
            404: openapi.Response(description="Платёж с указанным ID не найден"),
        },
    )
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)

        if not payment.session_id:
            return Response(
                {"detail": "У этого платежа отсутствует session_id Stripe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment_status = retrieve_stripe_session(payment.session_id)

        # Если у в модели Payment ,будет поле status, его можно сразу обновить:
        # payment.status = payment_status
        # payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "session_id": payment.session_id,
                "payment_status": payment_status,
            },
            status=status.HTTP_200_OK,
        )


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Список подписок пользователя",
        operation_description="Возвращает все активные подписки текущего авторизованного пользователя.",
        responses={
            200: openapi.Response(
                description="Список подписок",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "course_id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=2
                            ),
                            "user_last_name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Иванов"
                            ),
                            "user_first_name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Иван"
                            ),
                            "created_at": openapi.Schema(
                                type=openapi.TYPE_STRING, format="date-time"
                            ),
                        },
                    ),
                ),
            ),
            401: openapi.Response(description="Пользователь не авторизован"),
        },
    )
    def get(self, request, *args, **kwargs):
        subscriptions = Subscribe.objects.filter(user=request.user)
        data = [
            {
                "id": sub.id,
                "course_id": sub.course.id,
                "user_last_name": sub.user.last_name,
                "user_first_name": sub.user.first_name,
                "created_at": sub.created_at,
            }
            for sub in subscriptions
        ]
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Управление подпиской на курс",
        operation_description="Добавляет подписку на курс для текущего пользователя, если её нет, или удаляет, если она уже активна.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID курса", example=1
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Подписка добавлена или удалена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="подписка добавлена"
                        ),
                    },
                ),
            ),
            401: openapi.Response(description="Пользователь не авторизован"),
            404: openapi.Response(description="Курс с указанным ID не найден"),
        },
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscribe.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        # Возвращаем ответ в API
        return Response({"message": message})
