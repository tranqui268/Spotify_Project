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
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'profile_picture', 'verified', 'monthly_listeners', 'songs', 'profile_picture_url']
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
        if isinstance(instance.profile_picture, str):
            representation['profile_picture'] = instance.profile_picture  # Trả về trực tiếp URL nếu là URLField
        return representation
    
    def get_songs(self, obj):
        songs = Song.objects.filter(artist=obj)
        # Tránh đệ quy bằng cách truyền context và giới hạn serialize
        song_serializer = SongSerializer(songs, many=True, context={'request': self.context.get('request')})
        return song_serializer.data

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture  # Trả về trực tiếp URL nếu là URLField
        return None

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer1(read_only=True)
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), required=False, allow_null=True)
    cover_image = serializers.SerializerMethodField()
    songs = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'genre', 'total_song', 'release_date', 'cover_image', 'songs', 'cover_image_url']
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
        if isinstance(instance.cover_image, str):
            representation['cover_image'] = instance.cover_image  # Trả về trực tiếp URL nếu là URLField
        return representation
    
    def get_songs(self, obj):
        songs = Song.objects.filter(album=obj)
        # Tránh đệ quy bằng cách truyền context và giới hạn serialize
        song_serializer = SongSerializer(songs, many=True, context={'request': self.context.get('request')})
        return song_serializer.data

    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image  # Trả về trực tiếp URL nếu là URLField
        return None

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return obj.cover_image  # Trả về trực tiếp URL nếu là URLField
        return None

class SongSerializer(serializers.ModelSerializer):
    song_image = serializers.SerializerMethodField()

    def get_song_image(self, obj):
        if obj.song_image:
            return obj.song_image  # Trả về trực tiếp URL nếu là URLField
        return None

    audio_file = serializers.FileField(required=True, write_only=True)
    video_file = serializers.FileField(required=False, write_only=True, allow_null=True)
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False)
    class Meta:
        model = Song
        fields = [
            'id', 'title', 'artist', 'album', 'genre', 'song_image', 'audio_file',
            'video_file', 'duration', 'lyrics', 'total_plays', 'release_date'
        ]
        read_only_fields = ['id'] 

    def validate_audio_file(self, value):
        if not value:
            raise serializers.ValidationError("Audio file is required.")
        valid_audio_formats = ['mp3', 'wav', 'aac', 'm4a', 'ogg']
        file_extension = value.name.split('.')[-1].lower() if value.name else ''
        if file_extension not in valid_audio_formats:
            raise serializers.ValidationError(
                f"Unsupported audio format: {file_extension}. Supported formats are: {', '.join(valid_audio_formats)}."
            )
        return value

    def validate_song_image(self, value):
        if value:
            valid_image_formats = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = value.name.split('.')[-1].lower() if value.name else ''
            if file_extension not in valid_image_formats:
                raise serializers.ValidationError(
                    f"Unsupported image format: {file_extension}. Supported formats are: {', '.join(valid_image_formats)}."
                )
        return value

    def validate_video_file(self, value):
        if value:
            valid_video_formats = ['mp4', 'mov', 'avi', 'mkv']
            file_extension = value.name.split('.')[-1].lower() if value.name else ''
            if file_extension not in valid_video_formats:
                raise serializers.ValidationError(
                    f"Unsupported video format: {file_extension}. Supported formats are: {', '.join(valid_video_formats)}."
                )
        return value
    
    def create(self, validated_data):
        song_image = validated_data.pop('song_image', None)
        audio_file = validated_data.pop('audio_file')
        video_file = validated_data.pop('video_file', None)

        if song_image == "":
            song_image = None
        if audio_file == "":
            audio_file = None
        if video_file == "":
            video_file = None

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
        representation['audio_file'] = instance.audio_file.url if instance.audio_file else None
        representation['video_file'] = instance.video_file.url if instance.video_file else None
        return representation

class PlaylistSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    songs = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'user', 'songs', 'is_public', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def validate_songs(self, value):
        if not value:
            raise serializers.ValidationError("A playlist must contain at least one song.")
        
        # Chuyển đổi value thành danh sách ID
        song_ids = []
        for item in value:
            if isinstance(item, int):
                song_ids.append(item)
            elif hasattr(item, 'id'):  # Nếu là object Song
                song_ids.append(item.id)
            else:
                raise serializers.ValidationError(f"Invalid song value: {item}. Must be an ID or Song object with an ID.")

        # Kiểm tra ID hợp lệ
        invalid_ids = [song_id for song_id in song_ids if not Song.objects.filter(id=song_id).exists()]
        if invalid_ids:
            raise serializers.ValidationError(f"The following song IDs do not exist: {invalid_ids}")
        return song_ids  # Trả về danh sách ID đã xử lý

    def create(self, validated_data):
        user = self.context['request'].user
        songs_data = validated_data.pop('songs')
        playlist = Playlist.objects.create(user=user, **{k: v for k, v in validated_data.items() if k != 'user'})
        playlist.songs.set(songs_data)
        return playlist

    def to_representation(self, instance):
       representation = super().to_representation(instance)
       print(f"Songs queryset: {instance.songs.all()}")  # Debug
       representation['songs'] = SongSerializer(instance.songs.all(), many=True).data
       return representation



