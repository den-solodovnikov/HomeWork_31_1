

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("course/", include("lessons.urls", namespace="course")),
    # path("api/", include("api.urls"), name="api"),
]
