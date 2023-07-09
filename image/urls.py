from django.urls import path
from image.views import main_view

urlpatterns = [
    path('', main_view, name="main-view")
]
