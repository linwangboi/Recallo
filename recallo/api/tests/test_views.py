from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import StudyItem
from rest_framework import status


class UserSerializerTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='bob',
            email='bob@bob.com',
            password='bob'
        )
        self.item1 = StudyItem.objects.create(
            user=self.user,
            title='item1',
            description='description1'
        )
        self.item2 = StudyItem.objects.create(
            user=self.user,
            title='item2',
            description='description2'
        )
    def test_user_serializer_includeds_study_items(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('study_items', response.data)
        self.assertEqual(len(response.data['study_items']), 2)
        self.assertEqual(response.data['study_items'][0]['title'], 'item2')
        