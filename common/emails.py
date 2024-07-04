import pyotp
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGridEmailException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, detail=None, code=None, headers=None):
        self.headers = headers
        super().__init__(detail=detail, code=code)

    def __str__(self):
        errors = self.get_full_details()
        status_code = self.get_codes()
        message = errors.get('message')
        return f'Message: {message}; HttpStatusCode :{status_code}'


class SendGridEmailClient:

    def __init__(self, sendgrid_api_key: str = None, sender_email: str = None):
        self.sendgrid_api_key = sendgrid_api_key or settings.SENDGRID_API_KEY
        self.sender_email = sender_email or settings.SENDER_EMAIL

    def send_mail_verification_code(self, to_email, subject, otp):
        html_content = open("templates/register/html/base.html").read().format(verification_code=otp)
        message = Mail(
            from_email=self.sender_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        sendgrid = SendGridAPIClient(self.sendgrid_api_key)
        response = sendgrid.send(message)
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise SendGridEmailException(code=response.status_code, detail=response.body, headers=response.headers)

