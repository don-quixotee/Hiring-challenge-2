from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    image = models.ImageField(upload_to = 'user/', blank=True)
    name = models.CharField(max_length=100, blank=True)




