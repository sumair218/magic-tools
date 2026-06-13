from django import forms


class OCRImageForm(forms.Form):
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form-control',
            }
        )
    )
    output_format = forms.ChoiceField(
        label='Export Format',
        choices=[
            ('txt', 'Text (.txt)'),
            ('pdf', 'PDF (.pdf)'),
            ('word', 'Word (.docx)'),
            ('csv', 'CSV (.csv)'),
            ('xlsx', 'Excel (.xlsx)'),
        ],
        initial='txt',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
    enhance_low_quality = forms.BooleanField(
        label='Enhance low-quality image',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )


class OCRPDFForm(forms.Form):
    pdf_file = forms.FileField(
        label='PDF File',
        widget=forms.FileInput(
            attrs={
                'accept': '.pdf',
                'class': 'form-control',
            }
        )
    )
