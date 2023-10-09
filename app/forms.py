from django import forms

from .models import Music, Playlist
from .validators import validate_mp3_file


class AddMusicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['playlist'].queryset = Playlist.objects.filter(owner=user)

    mp3_file = forms.FileField(
        label='',
        validators=[validate_mp3_file]
    )

    playlist = forms.ModelChoiceField(
        queryset=Playlist.objects.all(),
        label='Select a playlist',
        required=True
    )

    class Meta:
        model = Music
        fields = ['mp3_file']


class PlaylistForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Playlist.objects.filter(title=title).exists():
            raise forms.ValidationError('This title is already in use.')
        return title

    class Meta:
        model = Playlist
        fields = ['title']
