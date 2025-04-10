from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Custom_UserModel(User):
    phone=models.IntegerField()
    gender=models.CharField(max_length=10,choices=[['male','Male'],['female','Female']])
    date_of_birth=models.DateField()

    def __str__(self):
        return self.username
