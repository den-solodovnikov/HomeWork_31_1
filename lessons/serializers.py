from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from lessons.models import Course, Lesson
from lessons.validators import validate_only_youtube
from user.models import Subscribe


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {"content": {"validators": [validate_only_youtube]}}


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, instance):
        # Достаем объект запроса из контекста сериализатора
        request = self.context.get("request")

        # Проверяем, что запрос передан и пользователь авторизован
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user, course=instance).exists()

        return False

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "lesson_count", "lessons")
