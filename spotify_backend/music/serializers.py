from rest_framework import serializers
from .models import Song, Artist, Genre, Album, Playlist
from accounts.models import CustomUser
from django.core.validators import FileExtensionValidator
from accounts.serializers import UserProfileSerializer

class ArtistSerializer1(serializers.ModelSerializer) :
    profile_picture = serializers.ImageField(required=False, write_only=True, allow_null=True) 


    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'profile_picture', 'verified', 'monthly_listeners']
        read_only_fields = ['id']

class ArtistSerializer(serializers.ModelSerializer) :
    profile_picture = serializers.ImageField(required=False, write_only=True, allow_null=True) 
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'profile_picture', 'verified', 'monthly_listeners', 'songs']
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
    
    def get_songs(self, obj):
        songs = Song.objects.filter(artist=obj)
        # Tránh đệ quy bằng cách truyền context và giới hạn serialize
        song_serializer = SongSerializer(songs, many=True, context={'request': self.context.get('request')})
        return song_serializer.data

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer1(read_only=True)
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), required=False, allow_null=True)
    cover_image = serializers.ImageField(
        required=False,
        write_only=True,
        allow_null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'genre', 'total_song', 'release_date', 'cover_image', 'songs']
        read_only_fields = ['id']

    def create(self, validated_data):
        cover_image = validated_data.pop('cover_image', None)
        album = Album.objects.create(**validated_data)

        if cover_image:
            album.cover_image = cover_image
            album.save()

        return album

    def update(self, instance, validated_data):
        cover_image = validated_data.pop('cover_image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cover_image:
            instance.cover_image = cover_image
            instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = instance.genre.name if instance.genre else None
        representation['cover_image'] = instance.cover_image.url if instance.cover_image else None
        return representation
    
    def get_songs(self, obj):
        songs = Song.objects.filter(album=obj)
        # Tránh đệ quy bằng cách truyền context và giới hạn serialize
        song_serializer = SongSerializer(songs, many=True, context={'request': self.context.get('request')})
        return song_serializer.data

class SongSerializer(serializers.ModelSerializer):
    song_image = serializers.ImageField(required=False, write_only=True, allow_null=True)
    audio_file = serializers.FileField(required=True, write_only=True)
    video_file = serializers.FileField(required=False, write_only=True, allow_null=True)
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
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

class PlaylistSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    songs = SongSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'user', 'songs', 'is_public', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def validate_songs(self, value):
        if not value:
            raise serializers.ValidationError("A playlist must contain at least one song.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation




