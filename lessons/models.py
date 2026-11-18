from django.core.validators import FileExtensionValidator
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lessons/preview/",
        null=True,
        verbose_name="Превью",
        help_text="Добавьте изображение",
    )
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lessons/image/",
        null=True,
        verbose_name="Превью",
        help_text="Добавьте изображение",
    )
    video = models.FileField(
        verbose_name="Видео",
        upload_to="lessons/videos/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mov", "mkv", "webm"]
            )
        ],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
