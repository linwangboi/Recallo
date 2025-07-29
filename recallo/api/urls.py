from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"study-items", views.StudyItemViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = router.urls
