from django.urls import path

from .views import HomeView, AddMusicView, MusicListView, MusicDeleteView

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('addmusic/', AddMusicView.as_view(), name='addmusic'),
    path('listen/', MusicListView.as_view(), name='player'),
    path('delete/<int:pk>/', MusicDeleteView.as_view(), name="delete")
]
