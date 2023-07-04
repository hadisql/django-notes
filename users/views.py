from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, FormView
from django.http import HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import login

from .models import UserProfile

from .forms import UserProfileForm, RegisterForm



class RegisterPage(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True # we want to redirect authenticated users if trying to access the register page -> doesn't seem to work
    success_url = reverse_lazy('main:notes')

    def form_valid(self, form):
        # we override the form_valid function so it logs the user in after registering
        user = form.save()
        if user is not None:
            # if the user form is successfully saved, go ahead and login the user
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main:notes') #forces to redirect to main page when user is authenticated
        return super(RegisterPage, self).get(*args, **kwargs) #otherwise we apply the original method

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main:all-notes') #force the login to redirect to notes page instead of profile (that doesn't exist)

# Profile Pages
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
        return reverse('users:profile', kwargs={'pk':self.kwargs['pk']})
