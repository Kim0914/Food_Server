from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),
    (2, 'Nothing')
)

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

