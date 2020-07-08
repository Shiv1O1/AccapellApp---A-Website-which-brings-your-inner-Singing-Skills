from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class file(models.Model):
    name = models.CharField(max_length = 100)
    song = models.FileField(blank=True, null=True, upload_to="song/")
    vocals = models.FileField(blank=True, null=True, upload_to="vocals/")
    music = models.FileField(blank=True, null=True, upload_to="music/")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    privacy = models.BooleanField()