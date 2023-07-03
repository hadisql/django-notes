from django.urls import path

from .views import PersonalNoteList, NoteCreate, NoteUpdate, NoteDelete, CustomLoginView, RegisterPage, NoteList, NoteListDetail
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', NoteList.as_view(), name='all-notes'),
    path('my-notes/', PersonalNoteList.as_view(), name='notes'),
    path('note-create', NoteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>', NoteUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>', NoteDelete.as_view(), name='note-delete'),
    path('note-detail/<int:pk>', NoteListDetail.as_view(), name='note-detail'),
]
