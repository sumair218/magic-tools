from django import forms


class AIForm(forms.Form):
    prompt = forms.CharField(
        label='Prompt',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Ask the AI anything...',
            }
        )
    )
