from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from lessons.models import Course, Lesson


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя",
        help_text="Введите имя",
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Введите фамилию",
    )

    email = models.EmailField(
        unique=True, verbose_name="Email-адрес", help_text="Укажите адрес email"
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        null=True,
        verbose_name="Аватар",
        help_text="Добавьте изображение",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "cash", "Наличные"
        TRANSFER = "transfer", "Перевод на счет"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        validators=[MinValueValidator(0)],
    )
    payment_method = models.CharField(
        max_length=20,
        choices=Method.choices,
        default=Method.CASH,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии Stripe"
    )
    link = models.URLField(
        max_length=600, blank=True, null=True, verbose_name="Ссылка на оплату"
    )


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribes",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscribes", verbose_name="Курс"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.course}"
