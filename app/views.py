import os

import eyed3
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView

from .forms import AddMusicForm, PlaylistForm
from .models import Music, Playlist


class HomeView(TemplateView):
    template_name = 'app/home.html'


class AddMusicView(LoginRequiredMixin, CreateView):
    model = Music
    template_name = 'app/add_music.html'
    form_class = AddMusicForm
    success_url = reverse_lazy('app:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        mp3_file = form.cleaned_data['mp3_file']
        playlist_id = form.cleaned_data['playlist'].id

        playlist, created = Playlist.objects.get_or_create(id=playlist_id, owner=self.request.user)
        form.instance.playlist = playlist

        # save and get mp3 file data - time and title
        filename = mp3_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'musics', filename)
        with open(file_path, 'wb') as destination:
            for chunk in mp3_file.chunks():
                destination.write(chunk)
        audiofile = eyed3.load(file_path)
        form.instance.title = os.path.splitext(filename)[0] or "Unknown Title"
        time_in_seconds = int(audiofile.info.time_secs)
        minutes, seconds = divmod(time_in_seconds, 60)
        form.instance.time = f"{minutes}:{seconds:02d}" if time_in_seconds else 'N/A'
        form.instance.mp3_file = os.path.join('musics', filename)

        return super().form_valid(form)


class MusicListView(LoginRequiredMixin, ListView):
    model = Music
    template_name = 'app/player.html'
    context_object_name = 'element_list'

    def get_queryset(self):
        queryset = Music.objects.filter(owner=self.request.user).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_seconds = sum(
            (int(music.time.split(':')[0]) * 60 + int(music.time.split(':')[1]))
            for music in context['element_list']
        )

        total_time_minutes = total_seconds // 60
        total_time_seconds = total_seconds % 60

        context['total_time'] = f'{total_time_minutes}:{total_time_seconds:02d}'
        context['element_count'] = self.get_queryset().count()

        playlist_id = self.kwargs.get('pk')
        playlist = get_object_or_404(Playlist, pk=playlist_id, owner=self.request.user)
        context['selected_playlist'] = playlist

        return context


class MusicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Music
    success_url = reverse_lazy('app:player')
    template_name = None

    def test_func(self):
        music = self.get_object()
        if self.request.user == music.owner:
            return True
        return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        music = self.get_object()

        file_path = os.path.join(settings.MEDIA_ROOT, str(music.mp3_file))
        if os.path.exists(file_path):
            os.remove(file_path)

        music.delete()

        return redirect(self.success_url)


class CreatePlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'app/create_playlist.html'
    form_class = PlaylistForm
    success_url = reverse_lazy('app:addmusic')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
