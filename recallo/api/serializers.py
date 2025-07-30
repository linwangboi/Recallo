from rest_framework import serializers
from .models import StudyItem, User


class StudyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyItem
        fields = ["id", "user", "title", "description", "created_at", "updated_at"]
        read_only_fields = ['user', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    study_items = StudyItemSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'study_items']