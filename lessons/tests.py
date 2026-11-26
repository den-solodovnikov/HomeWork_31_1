from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lessons.models import Lesson, Course
from user.models import User, Subscribe


class LessonAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="Bred@test.com")
        self.course = Course.objects.create(title="Java", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="JSON", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_lesson(self):
        """Проверка создания урока."""
        url = reverse("course:lesson_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_create_lesson(self):
        """Проверка создания урока с валидной ссылкой YouTube."""
        url = reverse("course:lesson_create")
        data = {
            "title": "JSON",
            "description": "знакомство с JSON",
            "content": "https://youtube.com",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_create_lesson_forbidden_link(self):
        """Проверка блокировки урока при попытке добавить ссылку не на YouTube."""
        url = reverse("course:lesson_create")
        data = {
            "title": "Урок со сторонней ссылкой",
            "content": "Смотрите материалы здесь: https://google.com",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_list_lessons(self):
        """Проверка получения списка уроков."""
        url = reverse("course:lessons_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = data.get("results", data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], self.lesson.title)

    def test_update_lesson(self):
        """Проверка редактирования урока владельцем."""
        url = reverse("course:lesson_update", args=[self.lesson.pk])
        data = {"title": "JSON Advanced"}
        response = self.client.patch(url, data)
        data_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_response.get("title"), "JSON Advanced")
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "JSON Advanced")

    def test_delete_lesson(self):
        """Проверка удаления урока владельцем."""
        url = reverse("course:lesson_destroy", args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):
    """Тесты функционала подписки на обновления курса."""

    def setUp(self):
        self.user = User.objects.create(email="student@test.com")
        self.course = Course.objects.create(
            title="Курс для подписки", description="Описание"
        )
        self.url = reverse("user:subscription")

    def test_subscription_toggle(self):
        """Тест добавления и удаления подписки при повторном запросе."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.pk}

        # Подписка оформляется
        response_sub = self.client.post(self.url, data)
        self.assertEqual(response_sub.status_code, status.HTTP_200_OK)
        self.assertEqual(response_sub.json(), {"message": "подписка добавлена"})
        self.assertTrue(
            Subscribe.objects.filter(user=self.user, course=self.course).exists()
        )

        # Подписка удаляется
        response_unsub = self.client.post(self.url, data, format="json")
        self.assertEqual(response_unsub.status_code, status.HTTP_200_OK)
        self.assertEqual(response_unsub.json(), {"message": "подписка удалена"})
        self.assertFalse(
            Subscribe.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_list(self):
        """Тест получения списка подписок (GET-запрос)."""
        self.client.force_authenticate(user=self.user)
        Subscribe.objects.create(user=self.user, course=self.course)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["course_id"], self.course.pk)
