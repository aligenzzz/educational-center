from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from api_authentication.models import User


@receiver(post_save, sender=User)
def add_staff_permissions(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        all_permissions = Permission.objects.all()
        instance.user_permissions.set(all_permissions)
