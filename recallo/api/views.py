from rest_framework.viewsets import ModelViewSet
from .models import StudyItem, User
from .serializers import StudyItemSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


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
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
