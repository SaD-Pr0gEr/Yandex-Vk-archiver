"""Working with Yandex Disk endpoint: /v1/disk/resources"""
import os.path
from typing import Union

import requests

from .data_types import DIRECTORY, FILE
from .base import BaseUserDiskAPI


__all__ = ("YandexDiskResources",)


class YandexDiskResources(BaseUserDiskAPI):
    """Working with YandexDisk resources API."""

    def __init__(self, access_token: str) -> None:
        self.RESOURCES_BASE_URL = f"{self.API_BASE_URL}resources/"
        super().__init__(access_token)
        self.basic_header = {"Authorization": f"OAuth {self.access_token}"}

    def resource_meta_info(self, file_or_folder_path: str,
                           field_names: Union[list, tuple] = (),
                           offset: int = 0) -> Union[dict, int]:
        """File or folder meta info.
        file_or_folder_path: Path to file(or folder) on your Yandex Disk
        field_names: JSON data fieldnames(read API doc.)
        offset: number of elements to skip

        Returns dict data with more info(Read API doc. about these fields) or status code
        """
        response = requests.get(
            self.RESOURCES_BASE_URL,
            headers=self.basic_header,
            params={
                "path": file_or_folder_path,
                "fields": ", ".join(field_names),
                "offset": offset
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

    def create_folder(self, folder_name: str) -> Union[dict, int]:
        """Create folder on Yandex Disk.
        folder_name: Folder name(path) that should create

        Returns response status code(201 - Success)
        """
        response = requests.put(
            self.RESOURCES_BASE_URL,
            headers=self.basic_header,
            params={"path": folder_name}
        )
        match response.status_code:
            case 201:
                print("Successfully created")
            case 409:
                print("Folder with that name already exists."
                      " Or parent folder isn't created")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def delete_resource(self, file_or_folder_path: str, safe_waste: bool = True) -> int:
        """Delete file or folder.
        file_or_folder_path: Path to file(or folder) on your Yandex Disk
        safe_waste:
            If True, it'll be placed in trash basket(default True)
            else full deleted

        Returns response status code(204 - Success)
        """
        response = requests.delete(
            f"{self.RESOURCES_BASE_URL}",
            headers=self.basic_header,
            params={"path": file_or_folder_path, "permanently": safe_waste}
        )
        match response.status_code:
            case 204:
                if safe_waste:
                    print("Successfully placed in the trash")
                else:
                    print("Successfully deleted.")
            case 404:
                print("File(or folder) not found")
            case _:
                print("Something went wrong... Please try again!")
        return response.status_code

    def copy_file_or_folder(self, source_file_path: str,
                            copy_file_path: str, overwrite: bool = False) -> int:
        """Copy file or folder.
        file_or_folder_path: Source file(folder) path to copy
        copy_file_path: Paste file(folder) path
        overwrite: Overwrite file(folder) status

        Returns response status code(201 - Success)
        """
        response = requests.post(
            f"{self.RESOURCES_BASE_URL}copy/",
            headers=self.basic_header,
            params={
                "from": source_file_path,
                "path": copy_file_path,
                "overwrite": overwrite
            }
        )
        match response.status_code:
            case 201:
                print("Copied successfully")
            case 202:
                print("Folder resources copied!")
            case 404:
                print("File(or folder) not found")
            case 409:
                print("File(or folder) is already exists")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def get_download_file_link(self, file_or_folder_path: str) -> Union[str, int]:
        """Get file download link.
        file_path: absolute path to source file(or folder)

        Returns download link if it works success
        """
        response = requests.get(
            f"{self.RESOURCES_BASE_URL}download/",
            headers=self.basic_header,
            params={"path": file_or_folder_path}
        )
        match response.status_code:
            case 200:
                print("Download URL got successfully")
                return response.json()["href"]
            case 404:
                print("Download file not found")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def move_resource(self, resource_path: str, copy_file_path: str, overwrite: bool = False) -> int:
        """Move resource(file/folder) to other directory.
        resource_path: absolute path to source file(or folder)

        Returns status code(201/202 - Success)
        """
        response = requests.post(
            f"{self.RESOURCES_BASE_URL}move/",
            headers=self.basic_header,
            params={
                "from": resource_path,
                "path": copy_file_path,
                "overwrite": overwrite
            }
        )
        match response.status_code:
            case 201:
                print("Moved successfully")
            case 202:
                print("Folder resources moved!")
            case 404:
                print("File(or folder) not found")
            case 409:
                print("File(or folder) is already exists")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def get_public_resources(self, limit: int, offset: int, resource_type: str,
                             fields: Union[list, tuple] = ()) -> Union[dict, int]:
        """Gets user public resources.
        fields: JSON data fieldnames(read API doc.)
        limit: Data limit
        offset: Skip data count
        resource_type: 'dir' or 'file'

        Returns dict data(id success) or status code
        """
        params = {
            "fields": ", ".join(fields),
            "offset": offset
        }
        if limit:
            params["limit"] = limit
        if resource_type == DIRECTORY:
            params["type"] = DIRECTORY
        else:
            params["type"] = FILE
        response = requests.get(
            f"{self.RESOURCES_BASE_URL}public/",
            headers=self.basic_header,
            params=params
        )
        match response.status_code:
            case 200:
                return response.json()
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def publish_resource(self, file_path: str) -> Union[str, int]:
        """Publish resource on your Yandex Disk.
        file_path: Publish file path

        Returns public file link(success) or status code(error)
        """
        response = requests.put(
            f"{self.RESOURCES_BASE_URL}publish/",
            headers=self.basic_header,
            params={"path": file_path}
        )
        match response.status_code:
            case 200:
                return response.json()
            case 404:
                print("File not found")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def cancel_published_resource(self, file_path: str) -> int:
        """Cancel published resource.
        file_path: Published file path on your disk

        Returns status code(200 - Success)
        """

        response = requests.put(
            f"{self.RESOURCES_BASE_URL}unpublish/",
            headers=self.basic_header,
            params={"path": file_path}
        )
        match response.status_code:
            case 200:
                print("Success unpublished")
                return response.json()
            case 404:
                print("File not found")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def generate_file_upload_link(self, file_path: str, overwrite: bool = False) -> Union[str, int]:
        """Generate link for upload some file.
        file_path: File path

        Returns upload link(success) or status code(error)
        """
        response = requests.get(
            f"{self.RESOURCES_BASE_URL}upload/",
            headers=self.basic_header,
            params={"path": file_path, "overwrite": overwrite}
        )
        match response.status_code:
            case 200:
                print("Success got link")
                return response.json()["href"]
            case 409:
                print("File with that name already exists")
            case _:
                print("Something went wrong... Please try again")
        return response.status_code

    def upload_local_file(self, local_file_path: str,
                          disk_file_path: str, overwrite: bool = False):
        """Upload some local file to Yandex Disk.
        local_file_path: Your local file path
        disk_file_path: File path on yandex disk
        overwrite: Overwrite file status if True disk file will be overwritten with your local file

        Returns status code(201 - Success)
        """
        if not os.path.exists(local_file_path):
            print("File not found! Check file path:", local_file_path)
            return
        disk_upload_url = self.generate_file_upload_link(disk_file_path, overwrite)
        if not isinstance(disk_upload_url, str):
            print("Error! Status code:", disk_upload_url)
            return
        upload_response = requests.put(
            disk_upload_url,
            headers=self.basic_header,
            files={"file": open(local_file_path, "rb")}
        )
        match upload_response.status_code:
            case 201:
                print("Success uploaded")
            case 202:
                print("Success accepted!")
            case _:
                print("Something went wrong... Please try again")
        return upload_response.status_code

    def upload_file_from_url(self, upload_file_link: str, disk_file_path: str) -> int:
        """Yandex disk uploads file by url.
        upload_file_link: File link to upload

        Returns status code(200/202 - Success)
        """
        response = requests.post(
            self.RESOURCES_BASE_URL + "upload",
            headers=self.basic_header,
            params={"path": disk_file_path, "url": upload_file_link}
        )
        match response.status_code:
            case 200, 202:
                print("Success uploaded")
            case 409:
                print("File with similar name already exists!")
            case _:
                print("Something went wrong... Please try again!")
        return response.status_code
