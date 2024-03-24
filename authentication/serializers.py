from rest_framework import serializers

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

try:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.models import EmailAddress
    from allauth.utils import get_username_max_length
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


# Custom RegisterSerializer to add first_name and last_name fields
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.USERNAME_REQUIRED,
    )
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


# Custom login serializer
# Modify this to change the login behaviour (i.e.: Send a confirmation email when a user logs in)
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=False, allow_blank=True)
#     email = serializers.EmailField(required=False, allow_blank=True)
#     password = serializers.CharField(style={'input_type': 'password'})

#     def authenticate(self, **kwargs):
#         return authenticate(self.context['request'], **kwargs)

#     def _validate_email(self, email, password):
#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_username(self, username, password):
#         if username and password:
#             user = self.authenticate(username=username, password=password)
#         else:
#             msg = _('Must include "username" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_username_email(self, username, email, password):
#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         elif username and password:
#             user = self.authenticate(username=username, password=password)
#         else:
#             msg = _('Must include either "username" or "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def get_auth_user_using_allauth(self, username, email, password):
#         from allauth.account import app_settings as allauth_account_settings

#         # Authentication through email
#         if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.EMAIL:
#             return self._validate_email(email, password)

#         # Authentication through username
#         if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.USERNAME:
#             return self._validate_username(username, password)

#         # Authentication through either username or email
#         return self._validate_username_email(username, email, password)

#     def get_auth_user_using_orm(self, username, email, password):
#         if email:
#             try:
#                 username = UserModel.objects.get(email__iexact=email).get_username()
#             except UserModel.DoesNotExist:
#                 pass

#         if username:
#             return self._validate_username_email(username, '', password)

#         return None

#     def get_auth_user(self, username, email, password):
#         """
#         Retrieve the auth user from given POST payload by using
#         either `allauth` auth scheme or bare Django auth scheme.

#         Returns the authenticated user instance if credentials are correct,
#         else `None` will be returned
#         """
#         if 'allauth' in settings.INSTALLED_APPS:

#             # When `is_active` of a user is set to False, allauth tries to return template html
#             # which does not exist. This is the solution for it. See issue #264.
#             try:
#                 return self.get_auth_user_using_allauth(username, email, password)
#             except url_exceptions.NoReverseMatch:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise exceptions.ValidationError(msg)
#         return self.get_auth_user_using_orm(username, email, password)

#     @staticmethod
#     def validate_auth_user_status(user):
#         if not user.is_active:
#             msg = _('User account is disabled.')
#             raise exceptions.ValidationError(msg)

#     @staticmethod
#     def validate_email_verification_status(user, email=None):
#         from allauth.account import app_settings as allauth_account_settings
#         if (
#             allauth_account_settings.EMAIL_VERIFICATION == allauth_account_settings.EmailVerificationMethod.MANDATORY
#             and not user.emailaddress_set.filter(email=user.email, verified=True).exists()
#         ):
#             raise serializers.ValidationError(_('E-mail is not verified.'))

#     def validate(self, attrs):
#         username = attrs.get('username')
#         email = attrs.get('email')
#         password = attrs.get('password')
#         user = self.get_auth_user(username, email, password)

#         if not user:
#             msg = _('Unable to log in with provided credentials.')
#             raise exceptions.ValidationError(msg)

#         # Did we get back an active user?
#         self.validate_auth_user_status(user)

#         # If required, is the email verified?
#         if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
#             self.validate_email_verification_status(user, email=email)

#         attrs['user'] = user
#         return attrs
