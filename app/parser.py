from urllib.parse import urljoin

from config import API_BASE_URL
from utils import RequestManager, choose_biggest_size


class VkParser(RequestManager):
    """Парсер ссылок на фото с ВКонтакте"""

    def __init__(self, token: str, version: int, user_id: int, count_max: int = 5):
        self.token = token
        self.version = version
        self.count_max = count_max
        self.user_id = user_id
        self.count_like = 0

    def get_photo_links(self) -> list:
        photo_links = self.get(
            urljoin(API_BASE_URL, "photos.get"),
            params={
                "access_token": self.token,
                "v": self.version,
                "album_id": "profile",
                "count": self.count_max,
                "extended": 1,
                "owner_id": self.user_id,
                "photo_sizes": 1,
            }
        )
        link_list = []
        for photo in photo_links.json()["response"]["items"]:
            biggest_size = choose_biggest_size(photo["sizes"])
            link_list.append({
                "ID Фото": photo["id"],
                "наибольший размер": biggest_size,
                "Тип": biggest_size["type"],
                "count_like": photo["likes"]["count"]
            })
        print(
            f"Спарсены Топ {self.count_max} фото с самым большим размером!\n"
            f"ВНИМАНИЕ! Если ваши фотографии на профиле меньше чем вы указали в параметрах то "
            f"програма выводит только те фотки которые у вас есть \n"
        )
        return link_list
