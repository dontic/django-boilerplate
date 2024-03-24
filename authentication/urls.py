from django.urls import include, path, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from django.views.generic import TemplateView


urlpatterns = [
    # this url is used to generate email content
    re_path(
        r"^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path("", include("dj_rest_auth.urls")),
    # this url is used to generate email content
    path("registration/", include("dj_rest_auth.registration.urls")),
    path(
        "registration/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
]
