import json
import os
import logging

# django
from django.conf import settings

# Third-party
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk.api.lists_api import ListsApi


BREVO_API_KEY = os.getenv("BREVO_API_KEY")

# Initialize the logger
logger = logging.getLogger(__name__)


class Brevo:
    def __init__(self):
        # Configure the SDK
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key["api-key"] = BREVO_API_KEY

        # Initialize the api clients
        self.list_api = ListsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        self.contact_api = sib_api_v3_sdk.ContactsApi(
            sib_api_v3_sdk.ApiClient(self.configuration)
        )
        self.email_api = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(self.configuration)
        )

    # ---------------------------------------------------------------------------- #
    #                                   CONTACTS                                   #
    # ---------------------------------------------------------------------------- #
    def create_contact(self, email, attributes={}, list_ids=[]):
        """
        https://developers.brevo.com/reference/createcontact
        Create a new contact in Brevo

        Args:
            email (str): The email of the contact
            attributes (dict): The attributes of the contact
                i.e.: {"FIRSTNAME":"Elly", "LASTNAME":"Roger"}
            list_ids (list): The list ids to add the contact to

        Returns:
            response if successful
            {"error": "error message"} if unsuccessful
        """
        # Create a contact object
        contact_to_create = sib_api_v3_sdk.CreateContact(
            email=email, attributes=attributes, list_ids=list_ids
        )

        # Create a new contact
        try:
            api_response = self.contact_api.create_contact(contact_to_create)
            return api_response
        except ApiException as e:
            body = json.loads(e.body)
            code = body.get("code", "")
            message = body.get("message", "")

            return {"error": code, "message": message}

    def add_contacts_to_list(self, list_id: int, emails: list[str]):
        """
        https://developers.brevo.com/reference/addcontacttolist-1
        Adds contacts to a contact list in Brevo

        Args:
            list_id (int): The id of the list
            emails (list): The list of emails to add to the list

        Returns:
            response if successful
            {"error": "error message"} if unsuccessful
        """
        try:
            contact_emails = sib_api_v3_sdk.AddContactToList()
            contact_emails.emails = emails
            api_response = self.list_api.add_contact_to_list(list_id, contact_emails)
            return api_response
        except ApiException as e:
            body = json.loads(e.body)
            code = body.get("code", "")
            message = body.get("message", "")

            return {"error": code, "message": message}

    def remove_contacts_from_list(self, list_id: int, emails: list[str]):
        """
        https://developers.brevo.com/reference/removecontactfromlist
        Removes contacts from a contact list in Brevo

        Args:
            list_id (int): The id of the list
            emails (list): The list of emails to remove from the list

        Returns:
            response if successful
            {"error": "error message"} if unsuccessful
        """
        try:
            remove_contacts = sib_api_v3_sdk.RemoveContactFromList()
            remove_contacts.emails = emails
            api_response = self.list_api_instance.remove_contact_from_list(
                list_id, remove_contacts
            )
            return api_response
        except ApiException as e:
            body = json.loads(e.body)
            code = body.get("code", "")
            message = body.get("message", "")

            return {"error": code, "message": message}

    # ---------------------------------------------------------------------------- #
    #                             TRANSACTIONAL EMAILS                             #
    # ---------------------------------------------------------------------------- #
    def send_template_email(
        self,
        to: list,
        template_id: int,
        params: dict = None,
        cc: list = None,
        bcc: list = None,
        reply_to: dict = None,
        headers: dict = None,
    ):
        """
        https://developers.brevo.com/reference/sendtransacemail
        Sends a transactional email using a template

        Args:
            to (list): The list of recipients
                [{"email": "example@example.com", "name": "John Doe"}]
            template_id (int): The id of the template

            --- Optional ---
            params (dict): The parameters of the email template
                i.e.: {"parameter": "My param value"}
            cc (list): The list of CC recipients
                Can either be a list of emails or a list of dictionaries with the following structure:
                [{"email": "cc@example.com", "name": "CC Recipient"}]
            bcc (list): The list of BCC recipients
                [{"email": "bcc@example.com", "name": "BCC Recipient"}]
            reply_to (dict): The reply-to email
                i.e.: {"email": "reply-to@example.com"}
            headers (dict): The headers of the email
                i.e.: {"Some-Custom-Name": "unique-id-1234"}


        """
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            template_id=template_id,
            params=params,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            headers=headers,
        )

        try:
            api_response = self.email_api.send_transac_email(send_smtp_email)
            return api_response
        except ApiException as e:
            body = json.loads(e.body)
            code = body.get("code", "")
            message = body.get("message", "")

            return {"error": code, "message": message}
