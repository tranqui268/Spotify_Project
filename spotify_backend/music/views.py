from rest_framework import generics, permissions, status
from .models import Song, Artist
from .serializers import SongSerializer, ArtistSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class SongListCreateView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

class SongRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

# Filter views
class SongByTitleView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        title = self.kwargs['title']
        return Song.objects.filter(title__icontains=title)

class SongByArtistView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        artist_id = self.kwargs['artist_id']
        return Song.objects.filter(artist_id=artist_id)

class SongByAlbumView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        album_id = self.kwargs['album_id']
        return Song.objects.filter(album_id=album_id)

class SongByGenreView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        return Song.objects.filter(genre_id=genre_id)

class ArtistListCreateView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]

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
        serializer = self.get_serializer(self.queryset(), many = True)
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
    permission_classes = [IsAuthenticated, IsAdminUser]

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