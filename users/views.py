from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden

from .models import UserProfile

from .forms import UserProfileForm


# Create your views here.
class ProfilePage(LoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = 'profile'
    template_name = "users/userprofile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs['pk']
        context['profile'] = UserProfile.objects.get(id=profile_id) #making sure that the profile we use in the context (to be shown) is only the profile the user making the request

        return context

class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    context_object_name = 'profile'

    def test_func(self):
        profile_id = self.kwargs['pk']
        profile = UserProfile.objects.get(id=profile_id)
        return self.request.user == profile.user  # Check if the profile-update page is accessed by the same logged user

    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to update this profile.")

    def get_success_url(self):
        # cannot use reverse_lazy with pk to get back to user's profile
        return reverse('profile', kwargs={'pk':self.kwargs['pk']})
