from django.urls import path
from crop.views import cropped_image_view

app_name = 'crop'

urlpatterns = [
    path('', cropped_image_view, name="cropped-avatar-view")
]
