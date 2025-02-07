from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['register', 'login']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
   

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name'],
                passsword=serializer.validated_data['password']
            )
            token,created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'user_id': user.user_id,
                    'email': user.email,
                    'name': user.name
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'user_id': user.user_id,
                    'email': user.email,
                    'name': user.name
                }
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)