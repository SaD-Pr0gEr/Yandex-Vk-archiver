"""Yandex Disk info module."""
import requests

from base import BaseUserDiskAPI


class UserDiskInfo(BaseUserDiskAPI):
    """Yandex disk info class."""

    def __init__(self, access_token: str):
        super().__init__(access_token)

    def disk_info(self) -> dict | None:
        """User's disk info."""
        response = requests.get(
            self.API_BASE_URL,
            headers={
                "Authorization": f"OAuth {self.access_token}"
            }
        )
        if response.status_code != 200:
            return
        return response.json()
