# tasks.py

# celery
from celery import shared_task

from .brevo import Brevo


"""
# Shared task template
@shared_task
task():
    try:
        ...do stuff...
    except SystemExit:
        log.info("SystemExit requested, stopping task...")
    except:
        log.error("An uncaught error occurred while running the task")
        raise
"""


@shared_task
def send_template_email_task(to_email: list, template_id: int, params: dict = None):
    """
    This is a Celery task that sends an email using a Brevo template
    """

    try:
        bv = Brevo()
        bv.send_template_email(to_email, template_id, params=params)
    except SystemExit:
        pass
    except:
        raise
