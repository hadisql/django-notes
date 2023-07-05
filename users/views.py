from typing import Any
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, UpdateView, FormView
from django.http import HttpResponse, HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .models import UserProfile, PreviousAvatar

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
    template_name = 'users/userprofile_form.html'

    def test_func(self):
        profile_id = self.kwargs['pk']
        profile = UserProfile.objects.get(id=profile_id)
        return self.request.user == profile.user  # Check if the profile-update page is accessed by the same logged user

    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to update this profile.")

    def get_object(self, queryset=None):
        user_profile = get_object_or_404(UserProfile, id=self.kwargs['pk'])
        return user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['previous_avatars'] = user_profile.previous_avatars.all()
        return context

    def form_valid(self, form):
        user_profile = self.get_object()  # Retrieve the current UserProfile instance
        current_avatar = user_profile.avatar  # Get the current avatar before the update
        previous_avatars = [p.image.name for p in PreviousAvatar.objects.filter(user_profile=user_profile)]

        # Check if avatar field has changed when uploading new image
        if 'avatar' in form.changed_data:
                if current_avatar and (current_avatar not in previous_avatars):
                    # the second condition makes sure we don't save an empty avatar or an already uploaded avatar (with same name at least)
                    previous_avatar_obj = PreviousAvatar(user_profile=user_profile, image=current_avatar)
                    previous_avatar_obj.save()

        # selecting from old avatars
        selected_avatar_id = self.request.POST.get('previous_avatar')
        if selected_avatar_id:
            if current_avatar and (current_avatar not in previous_avatars):
                PreviousAvatar(user_profile=user_profile, image=current_avatar).save()
            current_avatar = get_object_or_404(PreviousAvatar, id=selected_avatar_id)
            form.instance.avatar = current_avatar.image


        return super().form_valid(form)

    def is_limit_reached(self):
        max_previous_avatars = 3
        user_profile = self.get_object()
        return user_profile.previous_avatars.filter(user_profile=user_profile).count() > max_previous_avatars

    def post(self, request, *args, **kwargs):
        if self.is_limit_reached():
            return HttpResponse("You've reached max number of avatars")  # Redirect to a specific URL if the limit is reached
        else:
            return super().post(request, *args, **kwargs)

    def get_success_url(self):
        # cannot use reverse_lazy with pk to get back to user's profile
        return reverse('users:profile', kwargs={'pk':self.kwargs['pk']})
