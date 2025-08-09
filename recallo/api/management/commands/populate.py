# recallo/api/management/commands/populate.py
from django.core.management.base import BaseCommand

from api.factories import ReviewSessionFactory, StudyItemFactory
from api.models import StudyItem, User
import random

# ✅ NEW — import for scheduled date calculation
from api.schedules import get_next_review_date
from datetime import date


class Command(BaseCommand):
    help = "Populate the database with sample data including scheduling info."

    def handle(self, *args, **kwargs):
        admin = User.objects.filter(username="admin").first()
        if not admin:
            admin = User.objects.create_superuser(
                username="admin", email="admin@gmail.com", password="admin"
            )

        user1 = User.objects.filter(username="user1").first()
        if not user1:
            user1 = User.objects.create_user(
                username="user1", email="user1@gmail.com", password="test"
            )

        user2 = User.objects.filter(username="user2").first()
        if not user2:
            user2 = User.objects.create_user(
                username="user2", email="user2@gmail.com", password="test"
            )

        for _ in range(10):
            StudyItemFactory(user=user1)
        for _ in range(10):
            StudyItemFactory(user=user2)

        # ✅ UPDATED — Create review sessions with correct scheduling & missed handling
        for user in [user1, user2]:
            for item in StudyItem.objects.filter(user=user):
                last_sequence = 0
                last_done = True  # assume first review is "done" for scheduling
                for _ in range(5):
                    # simulate possible missed review
                    done = random.choice([True, False])

                    # determine next sequence number
                    next_sequence = min(last_sequence + 1, 5)

                    # compute scheduled_for date based on missed logic
                    scheduled_for = get_next_review_date(
                        sequence=next_sequence,
                        missed=not last_done,  # missed if previous wasn't done
                        last_action_date=date.today()
                    )

                    # create the review session with all fields
                    ReviewSessionFactory(
                        user=user,
                        study_item=item,
                        sequence_number=next_sequence,
                        done=done,  # ✅ NEW — include done flag
                        scheduled_for=scheduled_for  # ✅ NEW — include scheduling
                    )

                    # prepare for next iteration
                    last_sequence = next_sequence
                    last_done = done

                # ✅ UPDATED — mark as completed if last sequence was 5 and done
                if last_sequence >= 5 and last_done:
                    item.status = StudyItem.Status.COMPLETED
                    item.save()
