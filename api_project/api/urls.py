from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookViewSet

router = DefaultRouter()
router.register(r'book_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', obtain_auth_token, name='api-token-auth'),
]