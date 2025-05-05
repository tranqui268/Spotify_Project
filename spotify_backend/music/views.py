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
        return Playlist.objects.filter(models.Q(is_public=True) | models.Q(user=user))

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Gán user hiện tại
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a playlist by ID (Public playlists or playlists of authenticated user)",
        responses={
            200: openapi.Response(description="Playlist details"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def get(self, request, *args, **kwargs):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a playlist by ID (Only owner can update)",
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
        operation_description="Partially update a playlist by ID (Only owner can update)",
        request_body=PlaylistSerializer,
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
        operation_description="Delete a playlist by ID (Only owner can delete)",
        responses={
            204: openapi.Response(description="Playlist deleted"),
            403: openapi.Response(description="Forbidden"),
            404: openapi.Response(description="Playlist not found"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def delete(self, request, *args, **kwargs):
        playlist = self.get_object()
        playlist.delete()
        return Response({"status": "success", "message": "Playlist deleted"}, status=status.HTTP_204_NO_CONTENT)


