from rest_framework.routers import DefaultRouter
from Auth.views import CustomUserViewSet

router = DefaultRouter() 

router.register(r'auth', CustomUserViewSet, basename='auth')
