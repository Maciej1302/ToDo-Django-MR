from django.contrib.auth.decorators import user_passes_test
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from Myapp.models import Case, User


class CaseAPITestCase(APITestCase):
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

        self.case_1 = Case.objects.create(title="Open test case 1", status=Case.StatusChoice.OPEN, user=self.user)


    def test_create_case(self):
        url = reverse("cases_list_create")
        data = {
            "title": "New test case",
            "status": "OPEN",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Case.objects.count(), 2)
        self.assertEqual(Case.objects.last().title, "New test case")
        self.assertEqual(Case.objects.last().status, "OPEN")

    def test_retrieve_case(self):
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.client.get(url, format="json")
        self.assertEqual(Case.objects.count(), 1)
        self.assertEqual(Case.objects.first().title, "Open test case 1")
        self.assertEqual(Case.objects.first().status, "OPEN")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_case_list(self):
        self.case_2 = Case.objects.create(title="Open test case 2", status=Case.StatusChoice.OPEN, user=self.user)
        url = reverse("cases_list_create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Open test case 1")
        self.assertEqual(response.data[0]["status"], "OPEN")
        self.assertEqual(response.data[1]["title"], "Open test case 2")
        self.assertEqual(response.data[1]["status"], "OPEN")


    def test_update_case(self):
        updated_data = {"status": "CLOSED"}
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case = Case.objects.get(id=self.case_1.id)
        case.refresh_from_db()
        self.assertEqual(case.status, "CLOSED")


    def test_delete_case(self):
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.client.delete(url)
        self.assertEqual(Case.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)