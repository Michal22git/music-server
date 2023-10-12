from django.contrib.auth.models import User
from django.db import models


class Music(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=10)
    mp3_file = models.FileField(upload_to='musics', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(
        'Playlist', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(
        'Music', related_name='playlists', blank=True)

    def get_songs_count(self, **kwargs):
        return self.songs.count()

    def get_sum_time(self, **kwargs):
        total_seconds = sum(
            int(song.time.split(':')[0]) * 60 + int(song.time.split(':')[1]) for song in self.songs.all())

        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds//60
        total_seconds %= 60

        formatted_time = f"{hours:02d}:{minutes:02d}:{total_seconds:02d}"
        return formatted_time

    def __str__(self):
        return self.title
