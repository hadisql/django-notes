from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponseForbidden

from django.db.models import Q

from .models import Note

from .forms import NoteForm

from django.contrib.auth.models import User

from users.models import UserProfile



class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(published=True)
        # Retrieve the user IDs for all the authors of the notes
        author_ids = [note.user_id for note in context['notes']]
        # Retrieve the avatars for the authors
        avatars = User.objects.filter(id__in=author_ids).values('userprofile__avatar', 'id')
        # Create a dictionary mapping user IDs to their respective avatars
        avatar_dict = {avatar['id']: avatar['userprofile__avatar'] for avatar in avatars}
        # Add the avatar dictionary to the context
        context['avatars'] = avatar_dict
        # context['test_ids'] = author_ids
        return context


class NoteListDetail(LoginRequiredMixin, TemplateView):
    template_name = "main/note_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note_id = self.kwargs['pk']
        context['note'] = Note.objects.get(id=note_id)
         # Retrieve the user ID for the author of the note
        author_id = context['note'].user_id
        # Retrieve the userprofile for the author
        userprofile = UserProfile.objects.filter(user_id=author_id)
       # Add the avatar to the context
        context['avatar'] = userprofile.first().avatar
        # context['test_ids'] = author_ids
        return context

class PersonalNoteList(LoginRequiredMixin, ListView):
    # when using loginrequiredMixin, the unauthenticated user cannot access the index page (where the notes are)
    # we added " LOGIN_URL = 'login' " in the settings
    model = Note
    context_object_name = 'notes'
    template_name = 'main/my_notes.html'

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
    success_url = reverse_lazy('main:notes')

    def form_valid(self, form):
    # forcing the form to have the authenticated user as author for the notes he creates
        form.instance.user = self.request.user
        return super(NoteCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h1_title'] = "Create a note"
        context['page_title'] = "Create"
        return context


class NoteUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('main:notes')

    def test_func(self):
        note_id = self.kwargs['pk']
        note = Note.objects.get(id=note_id)
        return self.request.user == note.user  # Check if the logged-in user owns the note

    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to update this note.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h1_title'] = "Edit your note"
        context['page_title'] = "Edit"
        return context

class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    fields = '__all__'
    success_url = reverse_lazy('main:notes')
