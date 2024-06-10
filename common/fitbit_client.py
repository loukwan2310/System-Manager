import base64
from typing import Callable

# import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

from common.constants import FITBIT_API_URL, FITBIT_DEFAULT_ACCEPT_LOCALE


class FitbitAPIException(APIException):
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


class FitbitClient:
    def __init__(self, api_url: str = None, client_id: str = None, client_secret=None,
                 code_verifier: str = None, code_challenge: str = None):
        self.api_url = api_url or FITBIT_API_URL
        self.client_id = client_id or settings.FITBIT_CLIENT_ID
        self.client_secret = client_secret or settings.FITBIT_CLIENT_SECRET
        self.code_verifier = code_verifier or settings.FITBIT_CODE_VERIFIER
        self.code_challenge = code_challenge or settings.FITBIT_CODE_CHALLENGE

    @property
    def _default_headers(self):
        token = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": 'application/x-www-form-urlencoded',
        }
        return headers

    def get_token(self, code: str):
        url = f'{self.api_url}/oauth2/token'
        headers = self._default_headers
        expires_in = settings.FITBIT_ACCESS_TOKEN_EXPIRE_HOURS * 60 * 60
        params = {
            'client_id': self.client_id,
            'code': code,
            'grant_type': 'authorization_code',
            'code_verifier': self.code_verifier,
            'code_challenge': self.code_challenge,
            'expires_in': expires_in
        }

        res = requests.post(url=url, params=params, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def refresh_token(self, refresh_token):
        url = f'{self.api_url}/oauth2/token'
        headers = self._default_headers
        expires_in = settings.FITBIT_ACCESS_TOKEN_EXPIRE_HOURS * 60 * 60
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'expires_in': expires_in
        }
        res = requests.post(url=url, params=params, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def get_user_profile(self, user_id, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "accept-locale": FITBIT_DEFAULT_ACCEPT_LOCALE
        }
        url = f'{self.api_url}/1/user/{user_id}/profile.json'
        res = requests.get(url=url, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def get_devices(self, user_id, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "accept-locale": FITBIT_DEFAULT_ACCEPT_LOCALE
        }
        url = f'{self.api_url}/1/user/{user_id}/devices.json'
        res = requests.get(url=url, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def get_heart_rate_intraday_by_interval(self, user_id, access_token, start_date, end_date, detail_level,
                                            start_time, end_time):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "accept-locale": FITBIT_DEFAULT_ACCEPT_LOCALE
        }
        url = f'{self.api_url}/1/user/{user_id}/activities/heart/date/' \
              f'{start_date}/{end_date}/{detail_level}/time/{start_time}/{end_time}.json'
        res = requests.get(url=url, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def get_activity_intraday_by_interval(self, user_id, access_token, resource, start_date, end_date, detail_level,
                                          start_time, end_time):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "accept-locale": FITBIT_DEFAULT_ACCEPT_LOCALE
        }
        url = f'{self.api_url}/1/user/{user_id}/activities/{resource}/date/' \
              f'{start_date}/{end_date}/{detail_level}/time/{start_time}/{end_time}.json'
        res = requests.get(url=url, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def get_sleep_log_by_date(self, user_id, access_token, date):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "accept-locale": FITBIT_DEFAULT_ACCEPT_LOCALE
        }
        url = f'{self.api_url}/1.2/user/{user_id}/sleep/date/{date}.json'
        res = requests.get(url=url, headers=headers)
        if res.status_code != status.HTTP_200_OK:
            raise FitbitAPIException(code=res.status_code, detail=res.content, headers=res.headers)
        return res.json()

    def retry_strategy(self, policy: dict, func_client: Callable):
        """
        Retry strategy
        :param policy: Retry policy
        :param func_client: function fitbit
        """
        refresh_token = policy.get('refresh_token')
        fitbit_refresh_callback = policy.get('fitbit_refresh_callback')
        try:
            return func_client()
        except FitbitAPIException as error:
            status_code = error.get_codes()
            if not (status_code == status.HTTP_401_UNAUTHORIZED and refresh_token and fitbit_refresh_callback):
                raise error
            fitbit_token = self.refresh_token(refresh_token)
            user_id = fitbit_token.get('user_id')
            access_token = fitbit_token.get('access_token')
            refresh_token = fitbit_token.get('refresh_token')
            fitbit_refresh_callback(user_id=user_id, access_token=access_token, refresh_token=refresh_token)
            return func_client(access_token=access_token)
