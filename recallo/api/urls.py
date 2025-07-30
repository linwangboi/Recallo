from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"study-items", views.StudyItemViewSet, basename='studyitem')
router.register(r"users", views.UserViewSet, basename='user')

urlpatterns = router.urls
