import logging

# celery
from celery import shared_task

# brevo
from .brevo import Brevo


# Initialize the logger
log = logging.getLogger("brevo")


@shared_task
def create_contact_task(
    email: str,
    attributes: dict = {},
    list_ids: list = [],
    update_enabled: bool = False,
):
    bv = Brevo()
    bv.create_contact(
        email, attributes=attributes, list_ids=list_ids, update_enabled=update_enabled
    )


@shared_task
def send_template_email_task(to_email: list, template_id: int, params: dict = None):
    bv = Brevo()
    bv.send_template_email(to_email, template_id, params=params)
