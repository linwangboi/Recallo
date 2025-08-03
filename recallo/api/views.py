from rest_framework.viewsets import ModelViewSet
from .models import StudyItem, User, ReviewSession
from .serializers import StudyItemSerializer, UserSerializer, ReviewSessionSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


# Create your views here.
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
        study_item_id = self.request.data.get('study_item')
        study_item = get_object_or_404(StudyItem, id=study_item_id, user=self.request.user)
        serializer.save(
            user=self.request.user,
            study_item=study_item        
        )
