from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import StudyItem
from rest_framework import status
from pprint import pprint

class StudyItemsViewsTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.User = User  # Save class for reuse
        self.staff = User.objects.create_user(
            username='staff',
            email='staff@staff.com',
            password='staff',
            is_staff=True
        )
        self.bob = User.objects.create_user(
            username='bob',
            email='bob@bob.com',
            password='bob'
        )
        self.charlie = User.objects.create_user(
            username='charlie',
            email='charlie@charlie.com',
            password='charlie'
        )
        # Study items for bob
        self.bobitem1 = StudyItem.objects.create(
            user=self.bob,
            title='bobitem1',
            description='bobdescription1'
        )
        self.bobitem2 = StudyItem.objects.create(
            user=self.bob,
            title='bobitem2',
            description='bobdescription2'
        )
    def test_staff_can_see_all_study_items(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('studyitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    def test_user_cannot_see_others_study_items(self):
        self.client.force_login(self.charlie)
        response = self.client.get(reverse('studyitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_can_create_study_item(self):
        self.client.force_login(self.bob)
        response = self.client.post(reverse('studyitem-list'), {
            'title': 'new study item',
            'description': 'new description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'new study item')
    def test_staff_can_see_all_users(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
