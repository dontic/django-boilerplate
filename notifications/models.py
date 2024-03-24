from django.db import models


class SendgridConfiguration(models.Model):
    """
    Sendgrid Configuration Model
    """

    sendgrid_api_key = models.CharField(
        max_length=254, unique=True, help_text="The Sendgrid API key"
    )
    sendgrid_from_email = models.EmailField(
        max_length=254,
        unique=True,
        help_text="The email address to send notifications from",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
