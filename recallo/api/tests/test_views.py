from pprint import pprint

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ReviewSession, StudyItem


class StudyItemsViewsTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.User = User  # Save class for reuse
        self.staff = User.objects.create_user(
            username="staff", email="staff@staff.com", password="staff", is_staff=True
        )
        self.bob = User.objects.create_user(
            username="bob", email="bob@bob.com", password="bob"
        )
        self.charlie = User.objects.create_user(
            username="charlie", email="charlie@charlie.com", password="charlie"
        )
        # Study items for bob
        self.bobitem1 = StudyItem.objects.create(
            user=self.bob, title="bobitem1", description="bobdescription1"
        )
        self.bobitem2 = StudyItem.objects.create(
            user=self.bob, title="bobitem2", description="bobdescription2"
        )

    def test_staff_can_see_all_study_items(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("studyitem-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_cannot_see_others_study_items(self):
        self.client.force_login(self.charlie)
        response = self.client.get(reverse("studyitem-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_can_create_study_item(self):
        self.client.force_login(self.bob)
        response = self.client.post(
            reverse("studyitem-list"),
            {"title": "new study item", "description": "new description"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "new study item")

    def test_staff_can_see_all_users(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class ReviewSessionViewsTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.User = User  # Save class for reuse
        self.staff = User.objects.create_user(
            username="staff", email="staff@staff.com", password="staff", is_staff=True
        )
        self.bob = User.objects.create_user(
            username="bob", email="bob@bob.com", password="bob"
        )
        self.charlie = User.objects.create_user(
            username="charlie", email="charlie@charlie.com", password="charlie"
        )
        # Study items for bob
        self.bobitem1 = StudyItem.objects.create(
            user=self.bob, title="bobitem1", description="bobdescription1"
        )
        self.bobreview1 = ReviewSession.objects.create(
            user=self.bob, study_item=self.bobitem1, sequence_number=1
        )
        self.bobitem2 = StudyItem.objects.create(
            user=self.bob, title="bobitem2", description="bobdescription2"
        )
        self.bobreview2 = ReviewSession.objects.create(
            user=self.bob, study_item=self.bobitem2, sequence_number=1
        )

    def test_staff_can_see_all_review_sessions(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("reviewsession-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_cannot_see_others_review_sessions(self):
        self.client.force_login(self.charlie)
        response = self.client.get(reverse("reviewsession-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_can_create_review_sessions(self):
        self.client.force_login(self.bob)
        response = self.client.post(
            reverse("reviewsession-list"),
            {"user": self.bob.id, "study_item": self.bobitem1.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.bob.id)
        self.assertEqual(response.data["study_item"], self.bobitem1.id)
        self.assertEqual(len(ReviewSession.objects.filter(user=self.bob)), 3)
