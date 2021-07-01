import requests
from urllib.parse import urljoin
from alive_progress import alive_bar
import time

from config_keys import API_BASE_URL, TOKEN, V, User_ID, TOKEN_YANDEX
from need_functions import choose_biggest_size


class VkDownload:
    BASE_URL = API_BASE_URL

    def __init__(self, token=TOKEN, version=V, count_max=5, user_id=User_ID):
        self.token = token
        self.version = version
        self.count_max = count_max
        self.user_id = user_id
        self.link_list = []
        self.count_like = 0

    def get_photos(self):
        link = urljoin(API_BASE_URL, "photos.get")
        res = requests.get(
            link,
            params={
                "access_token": self.token,
                "v": self.version,
                "album_id": "profile",
                "count": self.count_max,
                "extended": 1,
                "owner_id": self.user_id,
                "photo_sizes": 1,
            },
        )
        res_json = res.json()["response"]["items"]
        for photo in res_json:
            self.count_like = photo["likes"]["count"]
            biggest_size = choose_biggest_size(photo["sizes"])
            new_dict = {
                "ID Фото": photo["id"],
                "наибольший размер": biggest_size,
                "Тип": biggest_size["type"],
            }
            self.link_list.append(new_dict)
        print(
            f"Топ {self.count_max} фото с самым большим размером : \n {self.link_list} \n"
            f"ВНИМАНИЕ! Если ваши фотографии на профиле меньше чем вы указали в параметрах то "
            f"програма выводит только те фотки которые у вас есть \n"
        )
        return self.link_list


class YandexUpload(VkDownload):

    def yandex_upload(self, file_path, token=TOKEN_YANDEX):
        HEADERS = {"Authorization": f"OAuth {token}"}
        DOWNLOAD_LINK = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        return_list = []
        print("Прогресс в процессе просим подождать!")
        with alive_bar(len(self.link_list)) as bar:
            for links in self.link_list:
                bar()
                time.sleep(1)
                photo_links = links["наибольший размер"]["url"]
                photo_types = links["Тип"]
                result = requests.post(
                    DOWNLOAD_LINK,
                    headers=HEADERS,
                    params={
                        "url": photo_links,
                        "disable_redirects": False,
                        "path": f"/{file_path}/{self.count_like}.jpeg",
                    },
                )
                if result.status_code != 202:
                    print(f"ошибка! Код: {result.status_code} {result.json()}")
                    return result
                return_dict = {
                    "Имя файла": f"{self.count_like}.jpeg",
                    "Тип фото": photo_types,
                }
                return_list.append(return_dict)
        print(f"Список фотографий загруженных на Диск: \n {return_list}")
        return return_list


if __name__ == "__main__":
    upload_photo = YandexUpload(TOKEN, V, 5, User_ID)
    upload_photo.get_photos()
    upload_photo.yandex_upload("file_path", TOKEN_YANDEX)
