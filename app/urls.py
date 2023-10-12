from django.urls import path

from .views import HomeView, AddMusicView, MusicListView, MusicDeleteView, CreatePlaylistView, PlaylistListView
app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('addmusic/', AddMusicView.as_view(), name='addmusic'),
    path('delete/<int:pk>/', MusicDeleteView.as_view(), name="delete"),
    path('createplaylist/', CreatePlaylistView.as_view(), name="createplaylist"),
    path('listen/',PlaylistListView.as_view(),name='playlist_list'),
    path('listen/<int:pk>/', MusicListView.as_view(), name='player'),
]
