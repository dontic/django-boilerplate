import os
from allauth.account.adapter import DefaultAccountAdapter

from django_brevo.tasks import send_template_email_task

VERIFY_EMAIL_URL = os.getenv("VERIFY_EMAIL_URL")
PASSWORD_RESET_CONFIRM_URL = os.getenv("PASSWORD_RESET_CONFIRM_URL")
BREVO_VERIFY_EMAIL_TEMPLATE_ID = int(os.getenv("BREVO_VERIFY_EMAIL_TEMPLATE_ID"))
BREVO_PASSWORD_RESET_TEMPLATE_ID = int(os.getenv("BREVO_PASSWORD_RESET_TEMPLATE_ID"))


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        """
        Send an email to the user

        Args:
            template_prefix (str): The prefix of the email template
            email (str): The email address of the user
            context (dict): The context to be used in the email template. Its structure is defined for every case below
        """

        print(f"Self: {self}")
        print(f"Template Prefix: {template_prefix}")
        print(f"Email: {email}")
        print(f"Context: {context}")

        # ------------------------- Email confirmation signup ------------------------ #
        """
        Context structure:
        {
            "user": User object,
            "activate_url": activate_url,
            "key": key,
        }
        """
        if "email_confirmation_signup" in template_prefix:
            # Build the email context
            email_context = {}
            email_context["ACTIVATE_URL"] = f"{VERIFY_EMAIL_URL}?key={context['key']}"

            # Set the template ID
            # template_id = SENDGRID_VERIFY_EMAIL_TEMPLATE_ID
            template_id = BREVO_VERIFY_EMAIL_TEMPLATE_ID

        # ------------------------------ Password reset ------------------------------ #
        """
        Context structure:
        {
            "current_site": current_site,
            "user": User object,
            "password_reset_url": password_reset_url,
            "request": request,
        }

        password_reset_url = http://127.0.0.1:8000/auth/password/reset/confirm/1f/c43kum-bf31e491b78e81f88ab1ce3aa973bcd1/
                                                                            ^uid         ^token
        """
        if "password_reset_key" in template_prefix:
            # Build the email context
            email_context = {}

            uid = context["password_reset_url"].split("/")[-3]
            token = context["password_reset_url"].split("/")[-2]

            email_context["PASSWORD_RESET_URL"] = (
                f"{PASSWORD_RESET_CONFIRM_URL}?uid={uid}&token={token}"
            )

            # Set the template ID
            template_id = BREVO_PASSWORD_RESET_TEMPLATE_ID

        # ------------------------------ Send the email ------------------------------ #
        if not template_id:
            raise ValueError("Template ID not set")

        send_template_email_task.delay(
            [{"email": email}],
            template_id,
            params=email_context,
        )
