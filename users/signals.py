from django.db.models.signals import post_save
from django.contrib.auth.models import User
#receiver
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,
                                   first_name=instance.first_name,
                                   last_name=instance.last_name,
                                   email=instance.email)
        print('UserProfile created !')

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    print('UserProfile updated !')
