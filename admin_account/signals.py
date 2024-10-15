from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from authen.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, **kwargs):
    if kwargs.get('created', False):  # If the user is newly created, we will not send an email
        return

    # Check if profile status has changed
    if instance.activate_profile:
        subject = "Ваш профиль активирован"
        message = "Здравствуйте, ваш профиль активирован!"
    else:
        subject = "Ваш профиль деактивирован"
        message = "Здравствуйте, ваш профиль деактивирован."

    # Send email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email],
        fail_silently=False,
    )
