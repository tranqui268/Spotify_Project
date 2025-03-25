from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Song, Playlist
from .serializers import SongSerializer, PlaylistSerializer

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    
class PlaylistList(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
