# leads/api_urls.py
from rest_framework.routers import DefaultRouter
from .api_views import CREViewSet

router = DefaultRouter()
router.register(r"cres", CREViewSet, basename="cre")

urlpatterns = router.urls
