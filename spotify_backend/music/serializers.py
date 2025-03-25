from rest_framework import serializers
from .models import Song, Playlist

class SongSerializer(serializers.ModelSerializer):
    class Metal:
        model = Song
        fields = ['id', 'title', 'artist', 'audio_file', 'image', 'duration', 'is_premium']

class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)
    class Meta:
        model = Playlist
        fields = ['id', 'user', 'name', 'songs']