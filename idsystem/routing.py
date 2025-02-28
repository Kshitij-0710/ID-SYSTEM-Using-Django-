from rest_framework.routers import DefaultRouter
from Auth.views import CustomUserViewSet,generate_id_card

router = DefaultRouter() 

router.register(r'auth', CustomUserViewSet, basename='auth')
