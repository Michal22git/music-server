from django.core.exceptions import ValidationError
from mutagen.mp3 import MP3


def validate_mp3_file(value):
    if not value.name.endswith('.mp3'):
        raise ValidationError('Invalid file extension. Only mp3 files are allowed.')

    try:
        audio = MP3(value)
        if audio.info.length > 900:
            raise ValidationError('File can not be longer than 15 minutes.')
    except Exception as e:
        raise ValidationError(f'Invalid mp3 file - {e}')
