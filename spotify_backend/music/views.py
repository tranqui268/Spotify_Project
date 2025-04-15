from rest_framework import generics, permissions
from .models import Song
from .serializers import SongSerializer

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

