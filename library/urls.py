from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet
from .views import BookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'book',BookViewSet)
urlpatterns = [
    path('', include(router.urls)),
]