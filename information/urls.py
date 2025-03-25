from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InformationItemViewSet, CommentViewSet

router = DefaultRouter()
router.register("items", InformationItemViewSet, basename="info")

urlpatterns = [
    path("", include(router.urls)),
    path("items/<uuid:info_id>/comments/", CommentViewSet.as_view({"get": "list", "post": "create"})),
]
