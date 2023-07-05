from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, PreviousAvatar

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


class RegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black'}))
    email = forms.EmailField(label = "Email", required=False, widget=forms.TextInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black', 'placeholder':'optional'}))
    first_name = forms.CharField(label = "First Name", required=False, widget=forms.TextInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black', 'placeholder':'optional'}))
    last_name = forms.CharField(label = "Last Name", required=False, widget=forms.TextInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black', 'placeholder':'optional'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black'}))

    class Meta:
        model = User
        fields = ("username", "first_name","last_name", "email", )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'rounded-xl py-1 px-2 dark:text-black'}))
