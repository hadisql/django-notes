from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import NoteList, NoteCreate, NoteUpdate, NoteDelete, CustomLoginView, RegisterPage

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', NoteList.as_view(), name='notes'),
    path('note-create', NoteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>', NoteUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>', NoteDelete.as_view(), name='note-delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
