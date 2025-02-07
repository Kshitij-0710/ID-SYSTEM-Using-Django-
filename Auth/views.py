from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer