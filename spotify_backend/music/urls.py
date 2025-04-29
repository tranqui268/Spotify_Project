from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, ArtistListCreateView, ArtistRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'song', SongViewSet, basename='song')
urlpatterns = [
    path('', include(router.urls)),
    path('artists/', ArtistListCreateView.as_view(), name='artist-list-create') ,
    path('artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view, name='artist-detail')
]
