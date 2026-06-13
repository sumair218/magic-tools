from django import forms


class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        label='PDF File',
        widget=forms.FileInput(
            attrs={
                'accept': '.pdf',
                'class': 'form-control',
            }
        )
    )


class WordUploadForm(forms.Form):
    doc_file = forms.FileField(
        label='Word File',
        widget=forms.FileInput(
            attrs={
                'accept': '.doc,.docx',
                'class': 'form-control',
            }
        )
    )


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def clean(self, data, initial=None):
        if data in self.empty_values:
            return None
        if isinstance(data, list):
            cleaned_files = []
            for uploaded_file in data:
                cleaned_files.append(super(MultiFileField, self).clean(uploaded_file, initial))
            return cleaned_files
        return super().clean(data, initial)


class MergePDFForm(forms.Form):
    pdf_files = MultiFileField(
        label='PDF Files',
        widget=MultiFileInput(
            attrs={
                'accept': '.pdf',
                'multiple': True,
                'class': 'form-control',
            }
        )
    )


class SplitPDFForm(forms.Form):
    pdf_file = forms.FileField(
        label='PDF File',
        widget=forms.FileInput(
            attrs={
                'accept': '.pdf',
                'class': 'form-control',
            }
        )
    )
    start_page = forms.IntegerField(
        label='Start Page',
        required=False,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '1',
            }
        )
    )
    end_page = forms.IntegerField(
        label='End Page',
        required=False,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last page',
            }
        )
    )


class CompressPDFForm(forms.Form):
    pdf_file = forms.FileField(
        label='PDF File',
        widget=forms.FileInput(
            attrs={
                'accept': '.pdf',
                'class': 'form-control',
            }
        )
    )
    quality = forms.ChoiceField(
        label='Compression Level',
        choices=[
            ('0', 'Low (fast)'),
            ('3', 'Medium'),
            ('9', 'High (best compression)'),
        ],
        initial='3',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
