from rest_framework import serializers

from .models import WaitlistedUser


class WaitlistedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitlistedUser
        fields = ("email", "first_name", "last_name", "phone_number")
