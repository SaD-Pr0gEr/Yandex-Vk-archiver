import time
from datetime import datetime

from alive_progress import alive_bar

from utils import RequestManager


class YandexUpload(RequestManager):
    """Загрузчик на Яндекс диск"""

    def upload(self, file_path: str, token: str, link_list: list):
        files_list = []
        print("Прогресс выгрузки в процессе... просим подождать!")
        with alive_bar(len(link_list)) as bar:
            for links in link_list:
                bar()
                time.sleep(1)
                result = self.post(
                    "https://cloud-api.yandex.net/v1/disk/resources/upload",
                    headers={"Authorization": f"OAuth {token}"},
                    params={
                        "url": links["наибольший размер"]["url"],
                        "disable_redirects": False,
                        "path": f"/{file_path}/VK-{datetime.today()}{links['count_like']}.jpeg",
                    },
                )
                if result.status_code != 202:
                    print(f"ошибка! Код: {result.status_code}\nОписание: {result.json()['description']}")
                    return result
                return_dict = {
                    "Имя файла": f"{links['count_like']}.jpeg",
                    "Тип фото": links["Тип"],
                }
                files_list.append(return_dict)
        print(f"Список фотографий загруженных на Диск: \n {files_list}")
        return files_list
