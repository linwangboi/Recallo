# recallo/api/urls.py

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"study-items", views.StudyItemViewSet, basename="studyitem")
router.register(r"users", views.UserViewSet, basename="user")
router.register(
    r"review-sessions", views.ReviewSessionViewSet, basename="reviewsession"
)

urlpatterns = router.urls
