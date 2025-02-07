from django.contrib import admin
from .models import CustomUser


class UserModel(admin.ModelAdmin):
    list_display=['user_id','email','name','is_paid']
# Register your models here.
admin.site.register(CustomUser,UserModel)