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

    def create_case(self, title="New test case", case_status="OPEN"):
        """method for creating cases"""
        url = reverse("cases_list_create")
        data = {
            "title": title,
            "status": case_status,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.case_id = Case.objects.first().id
        return response.data

    def test_create_case(self):
        self.create_case()
        self.assertEqual(Case.objects.count(), 1)
        self.assertEqual(Case.objects.first().title, "New test case")
        self.assertEqual(Case.objects.first().status, "OPEN")

    def test_retrieve_case(self):
        self.create_case()
        url = reverse("case_retrieve_update_destroy", args=[self.case_id])
        response = self.client.get(url, format="json")
        self.assertEqual(Case.objects.count(), 1)
        self.assertEqual(Case.objects.first().title, "New test case")
        self.assertEqual(Case.objects.first().status, "OPEN")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_case_list(self):
        self.create_case(title="New test case 1", case_status="OPEN")
        self.create_case(title="New test case 2", case_status="CLOSED")
        url = reverse("cases_list_create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "New test case 1")
        self.assertEqual(response.data[0]["status"], "OPEN")
        self.assertEqual(response.data[1]["title"], "New test case 2")
        self.assertEqual(response.data[1]["status"], "CLOSED")

    def test_update_case(selfs):
        selfs.create_case()
        updated_data = {"status": "CLOSED"}
        url = reverse("case_retrieve_update_destroy", args=[selfs.case_id])
        response = selfs.client.patch(url, updated_data, format="json")
        selfs.assertEqual(response.status_code, status.HTTP_200_OK)
        case = Case.objects.get(id=selfs.case_id)
        case.refresh_from_db()
        selfs.assertEqual(case.status, "CLOSED")

    def test_delete_case(selfs):
        selfs.test_create_case()
        url = reverse("case_retrieve_update_destroy", args=[selfs.case_id])
        response = selfs.client.delete(url)
        selfs.assertEqual(Case.objects.count(), 0)
        selfs.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
