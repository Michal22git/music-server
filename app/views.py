import os
import eyed3
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView

from .forms import AddMusicForm
from .models import Music


class HomeView(TemplateView):
    template_name = 'app/home.html'


class AddMusicView(LoginRequiredMixin, CreateView):
    template_name = 'app/add_music.html'
    form_class = AddMusicForm
    success_url = reverse_lazy('app:player')
    success_message = "Music has been added successfully!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        mp3_file = form.cleaned_data['mp3_file']

        filename = mp3_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'musics', filename)

        with open(file_path, 'wb') as destination:
            for chunk in mp3_file.chunks():
                destination.write(chunk)

        audiofile = eyed3.load(file_path)
        form.instance.title = os.path.splitext(filename)[0] or "Unknown Title"

        time_in_seconds = int(audiofile.info.time_secs)
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60
        form.instance.time = f"{minutes}:{seconds:02d}" or 'N/A'

        form.instance.mp3_file = os.path.join('musics', filename)

        return super().form_valid(form)


class MusicListView(LoginRequiredMixin, ListView):
    model = Music
    template_name = 'app/player.html'
    context_object_name = 'element_list'
    queryset = Music.objects.all()

    def get_queryset(self):
        return Music.objects.filter(owner=self.request.user)


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
        messages.success(self.request, 'Music and file have been deleted.')

        return redirect(self.success_url)
