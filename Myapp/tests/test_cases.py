from django.contrib.auth.decorators import user_passes_test
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from Myapp.models import Case, User


class CaseAPITestCase(APITestCase):
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
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.case_1 = Case.objects.create(
            title="Open test case 1", status=Case.StatusChoice.OPEN, user=self.user
        )

    def test_user_cannot_access_other_users_case(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, status=Case.StatusChoice.OPEN, title="Other user's case"
        )
        response = self.client.get(
            reverse("case_retrieve_update_destroy", args=[other_case.id])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_see_only_their_own_cases(self):
        user_case = Case.objects.create(user=self.user, title="User's case")
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(user=other_user, title="Other user's case")
        response = self.client.get(reverse("cases_list_create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case_ids = [case["pk"] for case in response.data]
        self.assertIn(user_case.id, case_ids)
        self.assertNotIn(other_case.id, case_ids)

    def test_user_cannot_edit_other_users_case(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, status=Case.StatusChoice.OPEN, title="Other user's case"
        )

        updated_data = {"title": "Updated title", "status": Case.StatusChoice.CLOSED}
        response = self.client.patch(
            reverse("case_retrieve_update_destroy", args=[other_case.pk]),
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other_users_case(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_case = Case.objects.create(
            user=other_user, status=Case.StatusChoice.OPEN, title="Other user's case"
        )
        response = self.client.delete(
            reverse("case_retrieve_update_destroy", args=[other_case.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

    def test_unauthenticated_user_create_case(self):
        url = reverse("cases_list_create")
        data = {
            "title": "New test case",
            "status": "OPEN",
        }
        response = self.unauthenticated_user.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_case(self):
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.client.get(url, format="json")
        self.assertEqual(Case.objects.count(), 1)
        self.assertEqual(Case.objects.first().title, "Open test case 1")
        self.assertEqual(Case.objects.first().status, "OPEN")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_retrieve_case(self):
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.unauthenticated_user.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_case_list(self):
        self.case_2 = Case.objects.create(
            title="Open test case 2", status=Case.StatusChoice.OPEN, user=self.user
        )
        url = reverse("cases_list_create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Open test case 1")
        self.assertEqual(response.data[0]["status"], "OPEN")
        self.assertEqual(response.data[1]["title"], "Open test case 2")
        self.assertEqual(response.data[1]["status"], "OPEN")

    def test_unauthenticated_user_retrieve_case_list(self):
        url = reverse("cases_list_create")
        response = self.unauthenticated_user.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_case(self):
        updated_data = {"status": "CLOSED"}
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case = Case.objects.get(id=self.case_1.id)
        case.refresh_from_db()
        self.assertEqual(case.status, "CLOSED")

    def test_unauthenticated_user_update_case(self):
        updated_data = {"status": "CLOSED"}
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.unauthenticated_user.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_case(self):
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.client.delete(url)
        self.assertEqual(Case.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_user_delete_case(self):
        url = reverse("case_retrieve_update_destroy", args=[self.case_1.id])
        response = self.unauthenticated_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
