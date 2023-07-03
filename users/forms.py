from django import forms
from django.core.files.images import get_image_dimensions

from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'w-full rounded-lg px-4 py-2 dark:text-black', 'rows':6}),
        required=False
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'w-full rounded-lg px-4 py-2 dark:text-black'}),
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'w-full rounded-lg px-4 py-2 dark:text-black'}),
        max_length=150,
        required=False
    )

    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'w-full rounded-lg px-4 py-2 dark:text-black'}),
        max_value=150,
        required=False
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'w-full rounded-lg px-4 py-2 dark:text-black'}),
        required=False
        )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'description' , 'first_name', 'last_name', 'age', 'email']
