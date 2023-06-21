from django.db import models

from django.conf import settings
from django.db.models.signals import post_save                      #This whole piece of code will generate the token for the new user when that user register to our app
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
