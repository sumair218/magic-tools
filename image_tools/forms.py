from django import forms


class ImageUploadForm(forms.Form):
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form-control',
            }
        )
    )


class ResizeImageForm(forms.Form):
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form-control',
            }
        )
    )
    width = forms.IntegerField(
        label='Width',
        required=False,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Width',
            }
        )
    )
    height = forms.IntegerField(
        label='Height',
        required=False,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Height',
            }
        )
    )


class CompressImageForm(forms.Form):
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form-control',
            }
        )
    )
    quality = forms.IntegerField(
        label='Compression Quality',
        min_value=10,
        max_value=95,
        initial=75,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '75',
            }
        )
    )
