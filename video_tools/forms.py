from django import forms


class DownloadURLForm(forms.Form):
    url = forms.URLField(
        label='Media URL',
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=...',
            }
        )
    )
    download_type = forms.ChoiceField(
        label='Download type',
        choices=[
            ('video', 'Video'),
            ('audio', 'Audio only'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
    video_quality = forms.ChoiceField(
        label='Video quality',
        choices=[
            ('best', 'Best available'),
            ('1080', '1080p'),
            ('720', '720p'),
            ('480', '480p'),
            ('360', '360p'),
        ],
        initial='best',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
