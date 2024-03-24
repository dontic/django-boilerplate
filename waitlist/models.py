from django.db import models
from django.conf import settings


class Waitlist(models.Model):
    name = models.CharField(max_length=255)
    brevo_list_id = models.IntegerField(
        blank=True,
        null=True,
        help_text="The list id in Brevo. If populated, the waitlist will be synced with this list.",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WaitlistedUser(models.Model):
    waitlist = models.ForeignKey(Waitlist, on_delete=models.CASCADE, default=1)
    email = models.EmailField(unique=True)

    # Optional fields
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    linked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
