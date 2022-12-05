"""Basic classes for Yandex Disk API modules."""


class BaseUserDiskAPI:
    """Base class for working with Yandex Disk API.
    access_token: OAuth token(Read more on documentation)
    """
    API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/"

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
