from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="userprofile", unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if (self.first_name and self.last_name) else f"{self.user.username} (username)"

    def get_fields(self):
        # looping through the attributes in order to display them in profile.html
        hide = ('id', 'user', 'avatar', 'description')
        return [(field.verbose_name, field.value_to_string(self)) for field in UserProfile._meta.fields if field.name not in hide]
