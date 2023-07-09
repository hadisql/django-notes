from django import forms
from users.models import UserProfile

class CroppedImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
