# recallo/api/views.py

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from datetime import date

from .models import ReviewSession, StudyItem, User
from .serializers import ReviewSessionSerializer, StudyItemSerializer, UserSerializer

# ✅ NEW — import scheduling logic
from api.business.review_scheduler import get_next_review_date


class StudyItemViewSet(ModelViewSet):
    serializer_class = StudyItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return StudyItem.objects.all()
        return StudyItem.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class ReviewSessionViewSet(ModelViewSet):
    serializer_class = ReviewSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ReviewSession.objects.all()
        return ReviewSession.objects.filter(user=user)

    def perform_create(self, serializer):
        study_item_id = self.request.data.get("study_item")
        study_item = get_object_or_404(
            StudyItem, id=study_item_id, user=self.request.user
        )

        previous_sessions = ReviewSession.objects.filter(
            user=self.request.user,
            study_item=study_item
        ).order_by('-sequence_number')

        if previous_sessions.exists():
            last_session = previous_sessions.first()
            last_sequence = last_session.sequence_number
            missed = not last_session.done  # ✅ NEW — detect if last was missed
            next_sequence = min(last_sequence + 1, 5)
        else:
            missed = False
            next_sequence = 1

        # ✅ NEW — compute scheduled_for date using missed handling
        scheduled_for = get_next_review_date(
            sequence=next_sequence,
            missed=missed,
            last_action_date=date.today()
        )

        # ✅ UPDATED — save with new scheduling and done flag default False
        review_session = serializer.save(
            user=self.request.user,
            study_item=study_item,
            sequence_number=next_sequence,
            reviewed_at=date.today(),
            scheduled_for=scheduled_for,
            done=False
        )

        # ✅ UPDATED — use model enum for status
        if next_sequence >= 5:
            study_item.status = StudyItem.Status.COMPLETED
            study_item.save()
