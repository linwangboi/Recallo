from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from api.models import ReviewSession, StudyItem


class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@test.com", password="test"
        )
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("test"))


class StudyItemModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="bob", email="bob@bob.com", password="bob"
        )
        self.item = StudyItem.objects.create(
            user=self.user,
            title="study DRF",
            description="Study django rest framework basics",
        )

    def test_str_representation(self):
        expected = "study DRF (bob@bob.com)"
        self.assertEqual(str(self.item), expected)

    def test_ordering(self):
        StudyItem.objects.create(
            user=self.user, title="second", description="the second study item object"
        )
        titles = [item.title for item in StudyItem.objects.all()]
        self.assertEqual(titles, ["second", "study DRF"])

    def test_related_name(self):
        self.assertIn(self.item, self.user.study_items.all())


class ReviewSessionModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="bob", email="bob@bob.com", password="bob"
        )
        self.item = StudyItem.objects.create(
            user=self.user,
            title="study DRF",
            description="Study django rest framework basics",
        )
        self.review = ReviewSession.objects.create(
            user=self.user, study_item=self.item, reviewed_at=timezone.now(), sequence_number=1
        )

    def test_string_representation_review_session(self):
        result = str(self.review)
        self.assertIn("Review for 'study DRF'", result)
        self.assertIn("bob@bob.com", result)
        self.assertIn(str(self.review.reviewed_at), result)
