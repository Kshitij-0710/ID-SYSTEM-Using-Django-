from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
import random
import string

class CustomUserManager(BaseUserManager):
    def create_user(self , email,name,passsword=None):
        if not email:
            raise ValueError("user must have an email")
        while True :
            user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k =5))
            if not self.model.objects.filter(user_id=user_id).exists():
                break
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_id=user_id
        )
        user.set_password(passsword)
        user.save(using=self.db)
        return user
    def create_superuser(self,email,name,password):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_staff =True
        user.is_superuser = True
        user.save(using=self.db)
        return user

    


