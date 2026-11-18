from rest_framework.routers import DefaultRouter

from lessons.apps import LessonsConfig
from lessons.views import CourseViewSet

app_name = LessonsConfig.name
router = DefaultRouter()
router.register('', CourseViewSet, basename='course')

urlpatterns = [

] + router.urls
