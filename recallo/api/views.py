from rest_framework.viewsets import ModelViewSet
from .models import StudyItem, User
from .serializers import StudyItemSerializer, UserSerializer


# Create your views here.
class StudyItemViewSet(ModelViewSet):
    queryset = StudyItem.objects.all()
    serializer_class = StudyItemSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
