from django.urls import path

from .views import PersonalNoteList, NoteCreate, NoteUpdate, NoteDelete, NoteList, NoteListDetail

app_name = 'main'

urlpatterns = [
    path('', NoteList.as_view(), name='all-notes'),
    path('my-notes/', PersonalNoteList.as_view(), name='notes'),
    path('note-create', NoteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>', NoteUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>', NoteDelete.as_view(), name='note-delete'),
    path('note-detail/<int:pk>', NoteListDetail.as_view(), name='note-detail'),
]
