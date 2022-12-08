"""YandexDisk API authentication module."""

import webbrowser
from typing import Union

import requests

from .base import YandexAPI


__all__ = ("YandexAuthorize",)


class YandexAuthorize(YandexAPI):
    OAUTH_BASE_URL = "https://oauth.yandex.ru/"
    AUTHORIZE_URL = f"{OAUTH_BASE_URL}authorize/"

    def __init__(self, client_id: str, application_password: str) -> None:
        self.application_secret = application_password
        super().__init__(client_id)

    def get_verify_code_page(self) -> None:
        response = requests.get(self.AUTHORIZE_URL, params={
            "client_id": self.client_id,
            "response_type": "code"
        })
        if response.status_code != 200:
            print("Something went wrong... Try again later!")
            return
        webbrowser.open(response.url)

    def get_access_token(self, verify_code: int) -> Union[dict, None]:
        response = requests.post(
            f"{self.OAUTH_BASE_URL}token",
            data={
                "grant_type": "authorization_code",
                "code": verify_code,
                "client_id": self.client_id,
                "client_secret": self.application_secret
            },
            headers={
                "Content-type": "application/x-www-form-urlencoded",
            }
        )
        if response.status_code != 200:
            print("Something went wrong... Try again later!")
            return
        return response.json()

    def run_console_user_authenticate(self) -> None:
        self.get_verify_code_page()
        verify_code = input("Input verify code from browser: ")
        if not verify_code.isdecimal():
            print("It's not number!")
            return
        token = self.get_access_token(int(verify_code))
        if not token:
            print("Couldn't got token...")
            return
        print("Your OAuth token:", token["access_token"])
