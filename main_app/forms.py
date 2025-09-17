from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'birthday', 'favorites']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }