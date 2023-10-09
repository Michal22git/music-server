from django.urls import path

from .views import HomeView, AddMusicView, MusicListView, MusicDeleteView, CreatePlaylistView

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('addmusic/', AddMusicView.as_view(), name='addmusic'),
    path('listen/<int:pk>/', MusicListView.as_view(), name='player'),
    path('delete/<int:pk>/', MusicDeleteView.as_view(), name="delete"),
    path('createplaylist/', CreatePlaylistView.as_view(), name="createplaylist")
]
