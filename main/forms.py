from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Note


class NoteForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full rounded-xl px-4 py-2 dark:text-black'}),
        max_length=150
    )
    note = forms.CharField(
        widget=CKEditorWidget(),
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'note', 'published']
