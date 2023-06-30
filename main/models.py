from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="notes")
    title = models.CharField(max_length=150, blank=True)
    note = RichTextField(blank=True, null=True)
    #note = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title if self.title else '(no title)'

    class Meta:
        ordering = ['-created_time'] # '-' prefix for a descending order
