from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, ArtistListCreateView, ArtistRetrieveUpdateDestroyView, GenreDetailView, GenreListCreateView

routerSong = DefaultRouter()
routerSong.register(r'songs', SongViewSet, basename='song')
urlpatterns = [
    path('', include(routerSong.urls)),
    path('artists/', ArtistListCreateView.as_view(), name='artist-list-create') ,
    path('artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view, name='artist-detail'),
    path('genres/', GenreListCreateView.as_view(), name='genre-list-create'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail')
]
