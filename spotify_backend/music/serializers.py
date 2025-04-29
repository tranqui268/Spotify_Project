from rest_framework import serializers
from .models import Song
from .models import Artist

class SongSerializer(serializers.ModelSerializer):
    song_image = serializers.ImageField(required=False, write_only=True, allow_null=True)
    audio_file = serializers.FileField(required=True, write_only=True)
    video_file = serializers.FileField(required=False, write_only=True, allow_null=True)
    class Meta:
        model = Song
        fields = [
            'id', 'title', 'artist', 'album', 'genre', 'song_image', 'audio_file',
            'video_file', 'duration', 'lyrics', 'total_plays', 'release_date'
        ]
        read_only_fields = ['id'] 
    
    def create(self, validated_data):
        song_image = validated_data.pop('song_image', None)
        audio_file = validated_data.pop('audio_file')
        video_file = validated_data.pop('video_file', None)

        song = Song.objects.create(
            **validated_data,
            song_image=song_image,
            audio_file=audio_file,
            video_file=video_file
        )
        return song

    def update(self, instance, validated_data):
        song_image = validated_data.pop('song_image', None)
        audio_file = validated_data.pop('audio_file', None)
        video_file = validated_data.pop('video_file', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if song_image:
            instance.song_image = song_image
        if audio_file:
            instance.audio_file = audio_file
        if video_file:
            instance.video_file = video_file

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['song_image'] = instance.song_image.url if instance.song_image else None
        representation['audio_file'] = instance.audio_file.url if instance.audio_file else None
        representation['video_file'] = instance.video_file.url if instance.video_file else None
        return representation


class ArtistSerializer(serializers.ModelSerializer) :
    profile_picture = serializers.ImageField(required=False, write_only=True, allow_null=True) 

    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'profile_picture', 'verified', 'monthly_listeners']
        read_only_fields = ['id']

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        artist = Artist.objects.create(**validated_data)

        if profile_picture:
            artist.profile_picture = profile_picture
            artist.save()
        
        return artist
    
    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_picture:
            instance.profile_picture = profile_picture 
            instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_picture:
            representation['profile_picture'] = instance.profile_picture.url
        else:
            representation['profile_picture'] = None
        return representation

