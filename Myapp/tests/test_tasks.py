from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Myapp.models import Case, Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.case = Case.objects.create(
            title="Test case", status=Case.StatusChoice.OPEN, user=self.user
        )
        self.task = Task.objects.create(case_id=self.case.id,
            title="New test task 1", description="New test task description 1", status="CREATED",user=self.user)

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


    def test_delete_task(self):
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task(self):
        updated_data = {
            "description": "Updated title",
            "status": "FINISHED"
        }
        url = reverse('task_retrieve_update_destroy', args=[self.task.id])
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "FINISHED")


    def test_change_status_of_finished_task(self):
        self.task.status = Task.StatusChoice.FINISHED
        self.task.save()
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        data = {"status": Task.StatusChoice.CREATED}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_task(self):
        url = reverse("task_retrieve_update_destroy", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New test task 1")
        self.assertEqual(response.data["description"], "New test task description 1")
        self.assertEqual(response.data["status"], Task.StatusChoice.CREATED)
        self.assertEqual(response.data["case"], self.case.id)
