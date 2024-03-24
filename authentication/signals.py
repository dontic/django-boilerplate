import os

# django
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save

# Brevo
from django_brevo.tasks import send_template_email_task

BREVO_PASSWORD_CHANGED_TEMPLATE_ID = int(
    os.getenv("BREVO_PASSWORD_CHANGED_TEMPLATE_ID")
)


@receiver(pre_save, sender=get_user_model())
def detect_password_change(sender, instance, **kwargs):
    """
    Checks if the user changed his password

    Cannot use the password_changed signal because it is not triggered
    when the user changes his password via dj_rest_auth.
    """
    if instance._password is None:
        return

    try:
        user = get_user_model().objects.get(id=instance.id)
    except get_user_model().DoesNotExist:
        return

    print("password changed")
    to = [
        {
            "email": user.email,
        }
    ]

    if not BREVO_PASSWORD_CHANGED_TEMPLATE_ID:
        return

    send_template_email_task.delay(to, BREVO_PASSWORD_CHANGED_TEMPLATE_ID)
