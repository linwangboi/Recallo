from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import StudyItem


class UserSerializerTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="bob", email="bob@bob.com", password="bob"
        )
        self.item1 = StudyItem.objects.create(
            user=self.user, title="item1", description="description1"
        )
        self.item2 = StudyItem.objects.create(
            user=self.user, title="item2", description="description2"
        )
        self.staff = User.objects.create(
            username="staff", email="staff@staff.com", password="staff", is_staff=True
        )

    def test_user_serializer_includeds_study_items(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("user-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("study_items", response.data)
        self.assertEqual(len(response.data["study_items"]), 2)
        self.assertEqual(response.data["study_items"][0]["title"], "item2")
