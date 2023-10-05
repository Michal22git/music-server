from django.contrib.auth.models import User
from django.db import models


class Music(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=10)
    mp3_file = models.FileField(upload_to='musics', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
