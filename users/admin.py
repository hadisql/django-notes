from django.contrib import admin

from .models import UserProfile, PreviousAvatar

admin.site.register(UserProfile)
admin.site.register(PreviousAvatar)
