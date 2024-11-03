from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from Myapp.models import Case, Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.unauthenticated_user = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.case = Case.objects.create(
            title="Test case", status=Case.StatusChoice.OPEN, user=self.user
        )
        self.task = Task.objects.create(
            case_id=self.case.id,
            title="New test task 1",
            description="New test task description 1",
            status="CREATED",
            user=self.user,
        )

    def test_user_sees_only_own_tasks_in_list(self):
        user_case = Case.objects.create(
            user=self.user, title="User's Case", status=Case.StatusChoice.OPEN
        )
        user_task = Task.objects.create(
            case=user_case,
            user=self.user,
            title="User's Task",
            status=Task.StatusChoice.CREATED,
        )

        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, title="Other User's Case", status=Case.StatusChoice.OPEN
        )
        other_task = Task.objects.create(
            case=other_case,
            user=other_user,
            title="Other User's Task",
            status=Task.StatusChoice.CREATED,
        )

        response = self.client.get(reverse("tasks_list_create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_ids = [task["pk"] for task in response.data]
        self.assertIn(user_task.id, task_ids)
        self.assertNotIn(other_task.id, task_ids)

    def test_user_cannot_access_another_users_task_detail(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, title="Other User's Case", status=Case.StatusChoice.OPEN
        )
        other_task = Task.objects.create(
            case=other_case,
            user=other_user,
            title="Other User's Task",
            status=Task.StatusChoice.CREATED,
        )

        response = self.client.get(
            reverse("task_retrieve_update_destroy", args=[other_task.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_another_users_task(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, title="Other User's Case", status=Case.StatusChoice.OPEN
        )
        other_task = Task.objects.create(
            case=other_case,
            user=other_user,
            title="Other User's Task",
            status=Task.StatusChoice.CREATED,
        )

        updated_data = {
            "title": "Updated Task Title",
            "status": Task.StatusChoice.FINISHED,
        }
        response = self.client.patch(
            reverse("task_retrieve_update_destroy", args=[other_task.pk]),
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_another_users_task(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, title="Other User's Case", status=Case.StatusChoice.OPEN
        )
        other_task = Task.objects.create(
            case=other_case,
            user=other_user,
            title="Other User's Task",
            status=Task.StatusChoice.CREATED,
        )

        response = self.client.delete(
            reverse("task_retrieve_update_destroy", args=[other_task.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task(self):
        url = reverse("tasks_list_create")
        data = {
            "case": self.case.id,
            "title": "New test task 2",
            "description": "New test task description 2",
            "status": "CREATED",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, "New test task 2")
        self.assertEqual(Task.objects.last().description, "New test task description 2")
        self.assertEqual(Task.objects.last().status, "CREATED")

    def test_unauthenticated_user_create_task(self):
        url = reverse("tasks_list_create")
        data = {
            "case": self.case.id,
            "title": "New test task 2",
            "description": "New test task description 2",
            "status": "CREATED",
        }
        response = self.unauthenticated_user.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_task(self):
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_unauthenticated_user_delete_task(self):
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.unauthenticated_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_closed_case(self):
        self.case.status = Case.StatusChoice.CLOSED
        self.case.save()
        url = reverse("tasks_list_create")
        data = {
            "case": self.case.id,
            "title": "Test task created for closed case",
            "description": "This test task should not be created.",
            "status": "CREATED",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(
            response.data["case"][0], str("You cannot add task to closed case.")
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_create_task_closed_case(self):
        self.case.status = Case.StatusChoice.CLOSED
        self.case.save()
        url = reverse("tasks_list_create")
        data = {
            "case": self.case.id,
            "title": "Test task created for closed case",
            "description": "This test task should not be created.",
            "status": "CREATED",
        }
        response = self.unauthenticated_user.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task(self):
        updated_data = {"description": "Updated title", "status": "FINISHED"}
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "FINISHED")

    def test_unauthenticated_user_update_task(self):
        updated_data = {"description": "Updated title", "status": "FINISHED"}
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.unauthenticated_user.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_status_of_finished_task(self):
        self.task.status = Task.StatusChoice.FINISHED
        self.task.save()
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        data = {"status": Task.StatusChoice.CREATED}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(
            response.data["status"][0],
            str("You cannot change the status of a finished task."),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_change_status_of_finished_task(self):
        self.task.status = Task.StatusChoice.FINISHED
        self.task.save()
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        data = {"status": Task.StatusChoice.CREATED}
        response = self.unauthenticated_user.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task(self):
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New test task 1")
        self.assertEqual(response.data["description"], "New test task description 1")
        self.assertEqual(response.data["status"], Task.StatusChoice.CREATED)
        self.assertEqual(response.data["case"], self.case.id)

    def test_unauthenticated_user_retrieve_task(self):
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.unauthenticated_user.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
