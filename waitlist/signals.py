import os
import logging

# django
from django.dispatch import receiver
from django.db.models.signals import post_save

# waitlist
from .models import WaitlistedUser

# Brevo
from django_brevo.tasks import create_contact_task


# Initialize logger
log = logging.getLogger("waitlist")


@receiver(post_save, sender=WaitlistedUser)
def create_brevo_contact(sender, instance: WaitlistedUser, **kwargs):
    """
    Creates a contact in Brevo when a user is added to the waitlist.
    """

    waitlist = instance.waitlist

    if not waitlist.brevo_list_id:
        log.debug("No linked Brevo list. Skipping...")
        return

    create_contact_task.delay(email=instance.email, list_ids=[waitlist.brevo_list_id])
