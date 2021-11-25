from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class User(AbstractUser):
    pass


class Notes(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    creation_date_time = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

class Favorites(models.Model):
    favorite_note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    favorite_date_time = models.DateTimeField(auto_now_add=True)