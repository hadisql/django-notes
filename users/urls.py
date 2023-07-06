from django.urls import path
from django.urls import reverse_lazy

from .views import ProfilePage, ProfileUpdate, RegisterPage, CustomLoginView, ManageAvatarsView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/<int:pk>', ProfilePage.as_view(), name='profile'),
    path('profile-update/<int:pk>', ProfileUpdate.as_view(), name='profile-update'),

    path('reset_password/', PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='reset_password'),
    path('reset_password_sent/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('manage-avatars/<int:pk>/', ManageAvatarsView.as_view(), name='manage_avatars'),
]
