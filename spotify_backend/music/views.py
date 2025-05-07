from rest_framework import generics, permissions, status, viewsets

from .permission import IsOwnerOrReadOnly
from .models import Song, Artist, Genre, Album, Playlist
from .serializers import SongSerializer, ArtistSerializer, GenreSerializer, AlbumSerializer, PlaylistSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from rest_framework.response import Response
from django.db import models
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @swagger_auto_schema(
        operation_description="List all songs or create a new song (Authenticated users)",
        responses={
            200: openapi.Response(
                description="List of songs",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "title": "Song Title",
                                "artist": 1,
                                "album": 1,
                                "genre": 1,
                                "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                                "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                                "video_file": "",
                                "duration": "00:03:30",
                                "lyrics": "Song lyrics",
                                "total_plays": 0,
                                "release_date": "2023-01-01"
                            }
                        ]
                    }
                }
            ),
            201: openapi.Response(
                description="Song created successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "id": 1,
                            "title": "Song Title",
                            "artist": 1,
                            "album": 1,
                            "genre": 1,
                            "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                            "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                            "video_file": "",
                            "duration": "00:03:30",
                            "lyrics": "Song lyrics",
                            "total_plays": 0,
                            "release_date": "2023-01-01"
                        }
                    }
                }
            ),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a song (Update/Delete: Admin only)",
        responses={
            200: openapi.Response(
                description="Song details",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "id": 1,
                            "title": "Song Title",
                            "artist": 1,
                            "album": 1,
                            "genre": 1,
                            "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                            "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                            "video_file": "",
                            "duration": "00:03:30",
                            "lyrics": "Song lyrics",
                            "total_plays": 0,
                            "release_date": "2023-01-01"
                        }
                    }
                }
            ),
            404: openapi.Response(description="Song not found"),
            403: openapi.Response(description="Permission denied"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            song = self.get_object()
            serializer = self.get_serializer(song)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Song.DoesNotExist:
            return Response({"status": "error", "message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            song = self.get_object()
            serializer = self.get_serializer(song, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            return Response({"status": "error", "message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            song = self.get_object()
            song.delete()
            return Response({"status": "success", "message": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            return Response({"status": "error", "message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='by-title/(?P<title>[^/.]+)')
    @swagger_auto_schema(
        operation_description="Filter songs by title (case-insensitive)",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_PATH, description="Song title", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(
                description="List of songs matching title",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "title": "Song Title",
                                "artist": 1,
                                "album": 1,
                                "genre": 1,
                                "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                                "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                                "video_file": "",
                                "duration": "00:03:30",
                                "lyrics": "Song lyrics",
                                "total_plays": 0,
                                "release_date": "2023-01-01"
                            }
                        ]
                    }
                }
            ),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def by_title(self, request, title=None):
        queryset = Song.objects.filter(title__icontains=title)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='by-artist/(?P<artist_id>\d+)')
    @swagger_auto_schema(
        operation_description="Filter songs by artist ID",
        manual_parameters=[
            openapi.Parameter('artist_id', openapi.IN_PATH, description="Artist ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="List of songs by artist",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "title": "Song Title",
                                "artist": 1,
                                "album": 1,
                                "genre": 1,
                                "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                                "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                                "video_file": "",
                                "duration": "00:03:30",
                                "lyrics": "Song lyrics",
                                "total_plays": 0,
                                "release_date": "2023-01-01"
                            }
                        ]
                    }
                }
            ),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def by_artist(self, request, artist_id=None):
        queryset = Song.objects.filter(artist_id=artist_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='by-album/(?P<album_id>\d+)')
    @swagger_auto_schema(
        operation_description="Filter songs by album ID",
        manual_parameters=[
            openapi.Parameter('album_id', openapi.IN_PATH, description="Album ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="List of songs by album",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "title": "Song Title",
                                "artist": 1,
                                "album": 1,
                                "genre": 1,
                                "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                                "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                                "video_file": "",
                                "duration": "00:03:30",
                                "lyrics": "Song lyrics",
                                "total_plays": 0,
                                "release_date": "2023-01-01"
                            }
                        ]
                    }
                }
            ),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def by_album(self, request, album_id=None):
        queryset = Song.objects.filter(album_id=album_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='by-genre/(?P<genre_id>\d+)')
    @swagger_auto_schema(
        operation_description="Filter songs by genre ID",
        manual_parameters=[
            openapi.Parameter('genre_id', openapi.IN_PATH, description="Genre ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="List of songs by genre",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "title": "Song Title",
                                "artist": 1,
                                "album": 1,
                                "genre": 1,
                                "song_image": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                                "audio_file": "https://res.cloudinary.com/your_cloud_name/audio/upload/songs/song.mp3",
                                "video_file": "",
                                "duration": "00:03:30",
                                "lyrics": "Song lyrics",
                                "total_plays": 0,
                                "release_date": "2023-01-01"
                            }
                        ]
                    }
                }
            ),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def by_genre(self, request, genre_id=None):
        queryset = Song.objects.filter(genre_id=genre_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ArtistListCreateView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    @swagger_auto_schema(
        operation_description="List all artists or create a new artist (Authenticated users)",
        responses={
            200: openapi.Response(
                description="List of artists",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "name": "Artist Name",
                                "bio": "Artist bio",
                                "profile_picture": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                                "verified": False,
                                "monthly_listeners": 0
                            }
                        ]
                    }
                }
            ),
            201: openapi.Response(
                description="Artist created successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "id": 1,
                            "name": "Artist Name",
                            "bio": "Artist bio",
                            "profile_picture": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                            "verified": False,
                            "monthly_listeners": 0
                        }
                    }
                }
            ),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(
            {"status":"success", "data": serializer.data},
            status= status.HTTP_200_OK
        )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            artist = serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ArtistRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete an artist (Admin only)",
        responses={
            200: openapi.Response(
                description="Artist details",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "id": 1,
                            "name": "Artist Name",
                            "bio": "Artist bio",
                            "profile_picture": "https://res.cloudinary.com/your_cloud_name/image/upload/artists/image.jpg",
                            "verified": False,
                            "monthly_listeners": 0
                        }
                    }
                }
            ),
            404: openapi.Response(description="Artist not found"),
            403: openapi.Response(description="Permission denied"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            artist = self.get_object()
            serializer = self.get_serializer(artist)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Artist.DoesNotExist:
            return Response(
                {"status": "error", "message": "Artist not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            artist = self.get_object()
            serializer = self.get_serializer(artist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Artist.DoesNotExist:
            return Response(
                {"status": "error", "message": "Artist not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            artist = self.get_object()
            artist.delete()
            return Response(
                {"status": "success", "message": "Artist deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Artist.DoesNotExist:
            return Response(
                {"status": "error", "message": "Artist not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class GenreListCreateView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all genres or create a new genre (Authenticated users)",
        responses={
            200: openapi.Response(description="List of genres"),
            201: openapi.Response(description="Genre created"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new genre (Authenticated users)",
        request_body=GenreSerializer,
        responses={
            201: openapi.Response(description="Genre created"),
            400: openapi.Response(description="Bad request"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a genre by ID (Authenticated users)",
        responses={
            200: openapi.Response(description="Genre details"),
            404: openapi.Response(description="Genre not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        genre = self.get_object()
        serializer = self.get_serializer(genre)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a genre by ID (Authenticated users)",
        request_body=GenreSerializer,
        responses={
            200: openapi.Response(description="Genre updated"),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Genre not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def put(self, request, *args, **kwargs):
        genre = self.get_object()
        serializer = self.get_serializer(genre, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a genre by ID (Authenticated users)",
        request_body=GenreSerializer,
        responses={
            200: openapi.Response(description="Genre updated"),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Genre not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def patch(self, request, *args, **kwargs):
        genre = self.get_object()
        serializer = self.get_serializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a genre by ID (Authenticated users)",
        responses={
            204: openapi.Response(description="Genre deleted"),
            404: openapi.Response(description="Genre not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def delete(self, request, *args, **kwargs):
        genre = self.get_object()
        genre.delete()
        return Response({"status": "success", "message": "Genre deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @swagger_auto_schema(
        operation_description="List all albums or create a new album (Authenticated users)",
        responses={
            200: openapi.Response(description="List of albums"),
            201: openapi.Response(description="Album created"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new album (Authenticated users)",
        request_body=AlbumSerializer,
        responses={
            201: openapi.Response(description="Album created"),
            400: openapi.Response(description="Bad request"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @swagger_auto_schema(
        operation_description="Retrieve an album by ID (Authenticated users)",
        responses={
            200: openapi.Response(description="Album details"),
            404: openapi.Response(description="Album not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        album = self.get_object()
        serializer = self.get_serializer(album)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update an album by ID (Authenticated users)",
        request_body=AlbumSerializer,
        responses={
            200: openapi.Response(description="Album updated"),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Album not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def put(self, request, *args, **kwargs):
        album = self.get_object()
        serializer = self.get_serializer(album, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an album by ID (Authenticated users)",
        request_body=AlbumSerializer,
        responses={
            200: openapi.Response(description="Album updated"),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Album not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def patch(self, request, *args, **kwargs):
        album = self.get_object()
        serializer = self.get_serializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an album by ID (Authenticated users)",
        responses={
            204: openapi.Response(description="Album deleted"),
            404: openapi.Response(description="Album not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def delete(self, request, *args, **kwargs):
        album = self.get_object()
        album.delete()
        return Response({"status": "success", "message": "Album deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Chỉ hiển thị playlists công khai hoặc playlists của user hiện tại
        user = self.request.user
        # return Playlist.objects.filter(models.Q(is_public=True) | models.Q(user=user))
        return Playlist.objects.filter(models.Q(user=user))

    @swagger_auto_schema(
        operation_description="List all public playlists or playlists created by the authenticated user, or create a new playlist",
        responses={
            200: openapi.Response(description="List of playlists"),
            201: openapi.Response(description="Playlist created"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new playlist (Authenticated users)",
        request_body=PlaylistSerializer,
        responses={
            201: openapi.Response(description="Playlist created"),
            400: openapi.Response(description="Bad request"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        # Nếu không có dữ liệu trong body, tạo playlist rỗng với tên tự động
        if not request.data:
            # Đếm số playlist của user
            playlist_count = Playlist.objects.filter(user=user).count()
            new_playlist_name = f"Playlist#{playlist_count + 1}"
            
            # Tạo playlist rỗng
            playlist = Playlist.objects.create(
                name=new_playlist_name,
                user=user,
                is_public=False  # Mặc định là private
            )
            serializer = self.get_serializer(playlist)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Playlist.objects.all()
        return Playlist.objects.filter(models.Q(is_public=True) | models.Q(user=user))

    @swagger_auto_schema(
        operation_description="Retrieve a playlist by ID (public playlists or playlists of authenticated user)",
        responses={
            200: openapi.Response(description="Playlist details"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized"),
            403: openapi.Response(description="Forbidden")
        }
    )
    def get(self, request, *args, **kwargs):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add songs to an existing playlist by ID (only the owner or admin can add songs)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'songs': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="List of song IDs to add to the playlist"
                )
            },
            required=['songs']
        ),
        responses={
            200: openapi.Response(description="Songs added successfully"),
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Forbidden"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def post(self, request, *args, **kwargs):
        playlist = self.get_object()
        songs_ids = request.data.get('songs', [])

        # Kiểm tra quyền: Chỉ owner hoặc admin mới được thêm nhạc
        if playlist.user != request.user and not request.user.is_staff:
            return Response(
                {"status": "error", "message": "Bạn không có quyền thêm nhạc vào playlist này"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Kiểm tra songs_ids là mảng
        if not isinstance(songs_ids, list):
            return Response(
                {"status": "error", "message": "Danh sách bài nhạc phải là một mảng"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra các ID bài nhạc có hợp lệ không
        invalid_ids = [song_id for song_id in songs_ids if not Song.objects.filter(id=song_id).exists()]
        if invalid_ids:
            return Response(
                {"status": "error", "message": f"Các ID bài nhạc sau không tồn tại: {invalid_ids}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra bài nhạc đã có trong playlist chưa
        existing_songs = set(playlist.songs.values_list('id', flat=True))
        new_songs = [song_id for song_id in songs_ids if song_id not in existing_songs]
        if not new_songs:
            return Response(
                {"status": "success", "message": "Tất cả bài nhạc đã có trong playlist"},
                status=status.HTTP_200_OK
            )

        # Thêm các bài nhạc mới
        playlist.songs.add(*new_songs)
        serializer = self.get_serializer(playlist)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Update a playlist by ID (only the owner can update)",
        request_body=PlaylistSerializer,
        responses={
            200: openapi.Response(description="Playlist updated"),
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Forbidden"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def put(self, request, *args, **kwargs):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a playlist by ID (only the owner can update, e.g., change name)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="New name for the playlist"
                )
            }
        ),
        responses={
            200: openapi.Response(description="Playlist updated"),
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Forbidden"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def patch(self, request, *args, **kwargs):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a playlist by ID (only the owner can delete) or remove songs from playlist",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'songs': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="List of song IDs to remove from the playlist (optional)"
                )
            }
        ),
        responses={
            204: openapi.Response(description="Playlist deleted or songs removed"),
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Forbidden"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def delete(self, request, *args, **kwargs):
        playlist = self.get_object()

        # Kiểm tra quyền: Chỉ owner hoặc admin mới được xóa
        if playlist.user != request.user and not request.user.is_staff:
            return Response(
                {"status": "error", "message": "Bạn không có quyền thực hiện hành động này"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Kiểm tra xem có yêu cầu xóa bài nhạc không
        songs_ids = request.data.get('songs', None)
        if songs_ids is not None:
            # Xóa bài nhạc khỏi playlist
            if not isinstance(songs_ids, list):
                return Response(
                    {"status": "error", "message": "Danh sách bài nhạc phải là một mảng"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra các ID bài nhạc có hợp lệ không
            invalid_ids = [song_id for song_id in songs_ids if not Song.objects.filter(id=song_id).exists()]
            if invalid_ids:
                return Response(
                    {"status": "error", "message": f"Các ID bài nhạc sau không tồn tại: {invalid_ids}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra bài nhạc có trong playlist không
            existing_songs = set(playlist.songs.values_list('id', flat=True))
            songs_to_remove = [song_id for song_id in songs_ids if song_id in existing_songs]
            if not songs_to_remove:
                return Response(
                    {"status": "success", "message": "Không có bài nhạc nào trong playlist để xóa"},
                    status=status.HTTP_200_OK
                )

            # Xóa các bài nhạc
            playlist.songs.remove(*songs_to_remove)
            serializer = self.get_serializer(playlist)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        # Nếu không có songs trong body, xóa toàn bộ playlist
        playlist.delete()
        return Response({"status": "success", "message": "Playlist deleted"}, status=status.HTTP_204_NO_CONTENT)