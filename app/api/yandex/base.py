"""Basic Yandex API tools."""


class YandexAPI:
    API_BASE_URL = "cloud-api.yandex.net/v1/"

    def __init__(self, client_id: str) -> None:
        self.client_id = client_id
