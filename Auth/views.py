from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from reportlab.lib.pagesizes import credit_card
from reportlab.pdfgen import canvas
from .models import CustomUser

def generate_id_card(request, user_id):
    try:
        user = CustomUser.objects.get(user_id=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse("User not found", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={user.user_id}_id_card.pdf'

    p = canvas.Canvas(response, pagesize=credit_card)
    width, height = credit_card

    # Draw ID Card Content
    p.setFont("Helvetica-Bold", 14)
    p.drawString(20, height - 30, "User ID Card")

    p.setFont("Helvetica", 12)
    p.drawString(20, height - 60, f"Name: {user.name}")
    p.drawString(20, height - 90, f"Email: {user.email}")
    p.drawString(20, height - 120, f"Unique ID: {user.user_id}")
    
    status_text = "Paid" if user.is_paid else "Not Paid"
    p.setFillColorRGB(0, 1, 0) if user.is_paid else p.setFillColorRGB(1, 0, 0)
    p.drawString(20, height - 150, f"Status: {status_text}")

    p.showPage()
    p.save()
    return response


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

