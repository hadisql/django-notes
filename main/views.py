from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.db.models import Q

from .models import Note

from .forms import NoteForm

class RegisterPage(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True # we want to redirect authenticated users if trying to access the register page -> doesn't seem to work
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        # we override the form_valid function so it logs the user in after registering
        user = form.save()
        if user is not None:
            # if the user form is successfully saved, go ahead and login the user
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes') #forces to redirect to main page when user is authenticated
        return super(RegisterPage, self).get(*args, **kwargs) #otherwise we apply the original method

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes') #force the login to redirect to notes page instead of profile (that doesn't exist)



class NoteList(LoginRequiredMixin, ListView):
# when using loginrequiredMixin, the unauthenticated user cannot access the index page (where the notes are)
# we added " LOGIN_URL = 'login' " in the settings
    model = Note
    context_object_name = 'notes'
    template_name = 'main/notes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user) #making sure that the notes we use in the context (to be shown) are only notes from a specific user: the user making the request
        context['count'] = context['notes'].count()

        search = self.request.GET.get('search-area') or ''
        if search is not None:
            context['notes'] = context['notes'].filter(Q(title__icontains = search) | Q(note__icontains = search))

        context['search_input'] = search

        return context


class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    #fields = ['title', 'note'] # we don't show 'user' -> the selection is overridden anyway (by the form valid function below)
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
    # forcing the form to have the authenticated user as author for the notes he creates
        form.instance.user = self.request.user
        return super(NoteCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h1_title'] = "Create a note"
        context['page_title'] = "Create"
        return context


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    #fields = ['title', 'note']
    success_url = reverse_lazy('notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h1_title'] = "Edit your note"
        context['page_title'] = "Edit"
        return context

class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    fields = '__all__'
    success_url = reverse_lazy('notes')
