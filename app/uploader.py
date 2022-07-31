import time
from datetime import datetime

from requests import post

from config import TOKEN_YANDEX
from utils import progress_bar


class YandexUpload:
    """Yandex Disk uploader"""

    @staticmethod
    @progress_bar
    def upload(bar, file_path: str, token: str, data: list) -> list or int:
        files_list = []
        for links in data:
            bar()
            time.sleep(1)
            result = post(
                "https://cloud-api.yandex.net/v1/disk/resources/upload",
                headers={"Authorization": f"OAuth {token}"},
                params={
                    "url": links["biggest_size"]["url"],
                    "disable_redirects": False,
                    "path": f"/{file_path}/VK-{str(datetime.today()).split(' ')[0]}{links['count_like']}.jpeg",
                },
            )
            if result.status_code != 202:
                print(f"ERROR! Code: {result.status_code}\nTitle: {result.json()['description']}")
                return result.status_code
            return_dict = {
                "File Name": f"{links['count_like']}.jpeg",
                "Photo type": links["type"],
            }
            files_list.append(return_dict)
        print(f"List of photos loaded on disk: \n {files_list}")
        return files_list


if __name__ == "__main__":
    data_list = []
    YandexUpload.upload(file_path="photos", token=TOKEN_YANDEX, data=[
        {
            "biggest_size": {"url": "https://avatars.githubusercontent.com/u/86515876?v=4"},
            "photo_id": 1,
            "type": "x",
            "count_like": 100
        },
        {
            "biggest_size": {
                "url": "https://github.githubassets.com/images/modules/profile/achievements/starstruck-default.png"
            },
            "photo_id": 2,
            "type": "y",
            "count_like": 1200
        },
    ])
