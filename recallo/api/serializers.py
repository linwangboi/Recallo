# recallo/api/serializers.py
from rest_framework import serializers

from .models import ReviewSession, StudyItem, User


class ReviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSession
        # ✅ UPDATED — added 'done' and 'scheduled_for' so API can handle them
        fields = ["study_item", "user", "reviewed_at", "sequence_number", "done", "scheduled_for"]
        read_only_fields = ["user", "reviewed_at", "sequence_number", "scheduled_for"]

class StudyItemSerializer(serializers.ModelSerializer):
    review_sessions = ReviewSessionSerializer(many=True, read_only=True)

    class Meta:
        model = StudyItem
        fields = [
            "id",
            "user",
            "title",
            'status',
            "description",
            "created_at",
            "updated_at",
            "review_sessions",
        ]
        read_only_fields = ["user", "created_at", "updated_at", 'status']


class UserSerializer(serializers.ModelSerializer):
    study_items = StudyItemSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "study_items"]
