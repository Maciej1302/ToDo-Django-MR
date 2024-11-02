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

    def test_create_task(
        self,
        title="New test task",
        description="New test task description",
        status_choice="CREATED",
    ):
        url = reverse("tasks_list_create")
        data = {
            "case": self.case.id,
            "title": title,
            "description": description,
            "status": status_choice,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.task_id = Task.objects.first().id
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, "New test task")
        self.assertEqual(Task.objects.first().description, "New test task description")
        self.assertEqual(Task.objects.first().status, "CREATED")
        return response.data

    def test_delete_task(self):
        self.test_create_task()
        url = reverse("task_retrieve_update_destroy", args=[self.task_id])
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

    """
    Return 'status': [ErrorDetail(string='"CREATED" is not a valid choice.', code='invalid_choice')]}
    def test_update_task(self):
        self.case.status = Case.StatusChoice.OPEN
        self.case.save()
        self.test_create_task()
        updated_data = {
            "description": "Updated title",
            "status": "FINISHED"
        }
        url = reverse('case_retrieve_update_destroy', args=[self.task_id])
        response = self.client.patch(url, updated_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "FINISHED")
"""

    def test_change_status_of_finished_task(self):
        task = Task.objects.create(
            user=self.user,
            case=self.case,
            title="New test task",
            description="New test task description",
            status=Task.StatusChoice.FINISHED,
        )
        url = reverse("task_retrieve_update_destroy", args=[task.id])
        data = {"status": Task.StatusChoice.CREATED}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_task(self):
        self.test_create_task()
        url = reverse("task_retrieve_update_destroy", args=[self.task_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New test task")
        self.assertEqual(response.data["description"], "New test task description")
        self.assertEqual(response.data["status"], Task.StatusChoice.CREATED)
        self.assertEqual(response.data["case"], self.case.id)
