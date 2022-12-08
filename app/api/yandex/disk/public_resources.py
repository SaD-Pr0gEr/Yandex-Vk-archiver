"""Working with Yandex Disk endpoint: /v1/disk/public/resources"""
from typing import Union

import requests

from .base import BaseUserDiskAPI


__all__ = ("YandexPublicResourcesAPI",)


class YandexPublicResourcesAPI(BaseUserDiskAPI):
    """Working with YandexDisk public resources API."""

    def __init__(self, access_token: str) -> None:
        super().__init__(access_token)
        self.BASE_PUBLIC_RESOURCES_URL = f"{self.API_BASE_URL}public/resources"
        self.basic_header = {"Authorization": f"OAuth {self.access_token}"}

    def public_resource_meta_info(self, public_key: str, offset: int = 0,
                                  field_names: Union[list, tuple] = ()):
        """Get public resource info(folder/file).
        public_key: Resource public key(you can get it with method YandexDiskResources.resource_meta_info)
            Read more on API doc.
        offset: number of elements to skip
        field_names: JSON data fieldnames(read API doc.)

        Returns dict data with more info(Read API doc. about these fields) or status code
        """
        response = requests.get(
            self.BASE_PUBLIC_RESOURCES_URL,
            headers=self.basic_header,
            params={
                "public_key": public_key,
                "offset": offset,
                "fields": field_names
            }
        )
        match response.status_code:
            case 200:
                return response.json()
            case 404:
                print("Resource not found!")
            case _:
                print("Something went wrong... Please try again!")
        return response.status_code

    def public_resource_download_link(self, public_key: str) -> Union[str, int]:
        """Get public resource download link.
        public_key: Resource public key(you can get it with method YandexDiskResources.resource_meta_info)
            Read more on API doc.

        Returns download link or status code
        """
        response = requests.get(
            self.BASE_PUBLIC_RESOURCES_URL + "download/",
            headers=self.basic_header,
            params={"public_key": public_key}
        )
        match response.status_code:
            case 200:
                return response.json()["href"]
            case 404:
                print("Resource not found!")
            case _:
                print("Something went wrong... Please try again!")
        return response.status_code

    def save_to_downloads(self, public_key: str, resource_save_name: str = None, save_path: str = None):
        """Save file to 'downloads' directory.
        public_key: Resource public key(you can get it with method YandexDiskResources.resource_meta_info)
            Read more on API doc.
        resource_save_name: Resource save name
        save_path: Resource save path(default 'downloads')

        Returns status code(200/201/202 - OK)
        """
        params = {"public_key": public_key}
        if resource_save_name:
            params["name"] = resource_save_name
        if save_path:
            params["save_path"] = save_path
        response = requests.post(
            self.BASE_PUBLIC_RESOURCES_URL + "save-to-disk",
            headers=self.basic_header,
            params=params
        )
        match response.status_code:
            case 200, 202, 201:
                print("Success uploaded")
            case 404:
                print("Resource not found!")
            case _:
                print("Something went wrong... Please try again!")
        return response.status_code
