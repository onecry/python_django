from django import forms
from .models import Profile

class AboutMe(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio',)

class AboutMeUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)
