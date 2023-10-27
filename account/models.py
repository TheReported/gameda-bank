from django.conf import settings
from django.contrib.auth.models import User as NormalUser
from django.db import models


class Profile(models.Model):
    dni = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)


class User(NormalUser):
    dni = models.CharField(max_length=9, unique=True, help_text="Required. Ex: 12345678F")
