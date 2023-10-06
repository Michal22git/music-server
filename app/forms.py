from django import forms
from .models import Music
from .validators import validate_mp3_file


class AddMusicForm(forms.ModelForm):
    mp3_file = forms.FileField(
        label='',
        validators=[validate_mp3_file]
    )

    class Meta:
        model = Music
        fields = ['mp3_file']
