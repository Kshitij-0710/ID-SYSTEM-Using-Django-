from django.db import router
from rest_framework.routers import DefaultRouter
routing = DefaultRouter()

router.register(r'auth',AuthViewset,basename = 'auth')