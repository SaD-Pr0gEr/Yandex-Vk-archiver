"""YandexDisk API authentication module."""

import webbrowser

import requests

from base import YandexAPI


class YandexAuthorize(YandexAPI):
    AUTH_URL = "https://oauth.yandex.ru/authorize/"
    OAUTH_BASE_URL = "https://oauth.yandex.ru/"

    def __init__(self, client_id: str, application_password: str) -> None:
        self.application_secret = application_password
        super().__init__(client_id)

    def get_verify_code(self) -> int | None:
        response = requests.get(self.AUTH_URL, params={
            "client_id": self.client_id,
            "response_type": "code"
        })
        if response.status_code != 200:
            print("Something went wrong... Try again later!")
            return
        webbrowser.open(response.url)
        verify_code = input("Input verify code from browser: ")
        if not verify_code.isdecimal():
            print("It's not number!")
            return
        return int(verify_code)

    def get_access_token(self, verify_code: int) -> dict | None:
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
        code = self.get_verify_code()
        if not code:
            print("Couldn't got verify code...")
            return
        token = self.get_access_token(code)
        if not token:
            print("Couldn't got token...")
            return
        print("Your OAuth token:", token["access_token"])
