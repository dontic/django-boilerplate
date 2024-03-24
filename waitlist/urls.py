from django.urls import include, path, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from django.views.generic import TemplateView

from .views import WaitlistedUserView


urlpatterns = [
    # this url is used to generate email content
    path(
        "add-contact/<waitlist_pk>/",
        WaitlistedUserView.as_view(),
        name="add_to_waitlist",
    ),
]
