from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    NONE = 0
    CLIENT = 1
    ACCOUNTANT = 2
    ADMIN = 3
    DIRECTOR = 4

    ROLE_CHOICES = [
        (NONE, 0),
        (CLIENT, 1),
        (ACCOUNTANT, 2),
        (ADMIN, 3),
        (DIRECTOR, 4),
    ]
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, default=NONE)
    image = models.ImageField(upload_to='user/profile', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username