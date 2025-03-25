from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_file = models.URLField(max_length=200)
    image = models.URLField(max_length=200, null=True, blank=True)
    duration = models.IntegerField()
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name
