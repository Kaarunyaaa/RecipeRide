from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings



class CustomUser(User):
    pass

class addrecipe(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    img=models.FileField(upload_to='images')
    ingredients=models.CharField(max_length=30)
    procedure=models.CharField(max_length=30)