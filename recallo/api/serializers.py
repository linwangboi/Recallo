from rest_framework import serializers

from .models import ReviewSession, StudyItem, User


class ReviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSession
        fields = ["study_item", "user", "reviewed_at"]
        read_only_fields = ["user", "reviewed_at"]


class StudyItemSerializer(serializers.ModelSerializer):
    review_sessions = ReviewSessionSerializer(many=True, read_only=True)

    class Meta:
        model = StudyItem
        fields = [
            "id",
            "user",
            "title",
            "description",
            "created_at",
            "updated_at",
            "review_sessions",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    study_items = StudyItemSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "study_items"]
