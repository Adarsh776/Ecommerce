from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Custom_UserModel)
class CustomUser_ModelAdmin(admin.ModelAdmin):
    list_display=['phone','email','username','gender']



