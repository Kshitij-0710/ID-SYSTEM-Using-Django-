from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
import random
from django_lifecycle import hook , AFTER_CREATE , AFTER_UPDATE
import string

class CustomUserManager(BaseUserManager):
    def create_user(self , email,name,password=None,is_paid=False):
        if not email:
            raise ValueError("user must have an email")
        while True :
            user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k =5))
            if not self.model.objects.filter(user_id=user_id).exists():
                break
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_id=user_id,
            is_paid = is_paid
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self,email,name,password):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            is_paid = True
        )
        user.is_staff =True
        user.is_superuser = True
        user.save(using=self.db)
        return user
class CustomUser(AbstractBaseUser,PermissionsMixin):
    user_id = models.CharField(max_length=5,unique=True)
    name = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)
    email = models.EmailField(default=True ,unique= True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def __str__(self):
        return f"{self.name} ({self.user_id})"
    @hook(AFTER_UPDATE, when='is_paid', was=False, is_now=True)
    def on_payment_success(self):
        """
        Trigger actions when a user's payment status changes to paid
        Example: Send confirmation email, grant access, etc.
        """
        # Add your payment success logic here
        pass
    
