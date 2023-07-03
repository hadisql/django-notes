from django.urls import path


from .views import ProfilePage, ProfileUpdate


urlpatterns = [
    path('profile/<int:pk>', ProfilePage.as_view(), name='profile'),
    path('profile-update/<int:pk>', ProfileUpdate.as_view(), name='profile-update'),
]
