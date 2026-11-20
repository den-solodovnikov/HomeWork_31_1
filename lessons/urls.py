from django.urls import path
from rest_framework.routers import DefaultRouter

from lessons.apps import LessonsConfig
from lessons.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

app_name = LessonsConfig.name
router = DefaultRouter()
router.register("", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lessons/<int:pk>/destroy/",
        LessonDestroyAPIView.as_view(),
        name="lesson_destroy",
    ),
] + router.urls
