# django
from django.shortcuts import render

# rest_framework
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

# waitlist
from .models import Waitlist, WaitlistedUser
from .serializers import WaitlistedUserSerializer


class WaitlistedUserView(CreateAPIView):
    queryset = WaitlistedUser.objects.all()
    serializer_class = WaitlistedUserSerializer

    # Public view
    permission_classes = []

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["waitlist_pk"] = self.kwargs.get("waitlist_pk")
        return context

    def create(self, request, *args, **kwargs):
        waitlist_pk = kwargs.get("waitlist_pk")
        try:
            waitlist = Waitlist.objects.get(pk=waitlist_pk)
        except Waitlist.DoesNotExist:
            return Response(
                {"error": "Waitlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            data=request.data, context={"waitlist": waitlist}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
