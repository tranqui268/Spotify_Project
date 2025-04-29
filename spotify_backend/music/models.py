from django.db import models

from accounts.models import CustomUser
from cloudinary.models import CloudinaryField


class Artist(models.Model):
    """ Music Artists Model """
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    profile_picture = CloudinaryField('image',blank=True, null=True)
    verified = models.BooleanField(default=False)
    monthly_listeners = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Genre(models.Model):
    """ Music Genre Model """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    """ Music Album Model """
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='albums')
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE,null=True,blank=True)
    total_song = models.IntegerField(default=0)
    release_date = models.DateField()
    cover_image = models.URLField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.title
    
class Song(models.Model):
    """ Song Model """
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
    song_image = CloudinaryField('image',blank=True, null=True)
    audio_file = CloudinaryField('audio')
    video_file = CloudinaryField('video',null=True, blank=True)
    duration = models.DurationField()
    lyrics = models.TextField(blank=True)
    total_plays = models.PositiveIntegerField(default=0)
    realease_date = models.DateField()

    def __str__(self):
        return self.title

class Playlist(models.Model):
    """ User Playlist Model """
    name = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ForeignKey(Song,on_delete=models.CASCADE, related_name='playlists')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class FavoriteSong(models.Model):
    """ User Favorite Song Model """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','song')
    
class ListeningHistory(models.Model):
    """ User Listening History """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listening_history')
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
    duration_listened = models.DurationField()
    