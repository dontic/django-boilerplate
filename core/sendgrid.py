# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


class Sendgrid:
    def __init__(self):
        self.sg = SendGridAPIClient(SENDGRID_API_KEY)
        self.from_email = "no-reply@fisy.es"

    def get_design(self, id):
        response = self.sg.client.designs._(id).get()

        body_bytes = response.body
        json_str = body_bytes.decode("utf-8").replace("'", '"')
        body_json = json.loads(json_str)

        return body_json

    def list_designs(self):
        params = {"page_size": 100, "summary": True}
        response = self.sg.client.designs.get(query_params=params)

        body_bytes = response.body
        json_str = body_bytes.decode("utf-8").replace("'", '"')
        body_json = json.loads(json_str)

        return body_json

    def send_email(self, to_email, subject, html_content, context=None):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )

        try:
            response = self.sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return True
        except Exception as e:
            print(e.message)
            return False
