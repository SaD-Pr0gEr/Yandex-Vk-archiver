from urllib.parse import urljoin

from config import API_BASE_URL
from utils import RequestManager, choose_biggest_size


class VkParser(RequestManager):
    """VK Photo links parser"""

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
                "photo_id": photo["id"],
                "biggest_size": biggest_size,
                "type": biggest_size["type"],
                "count_like": photo["likes"]["count"]
            })
        print(
            f"Parsed TOP {self.count_max} photos with biggest size!\n"
            f"WARNING! If your photos less than you gave in the parameter "
            f"program receives only those photos that  you have \n"
        )
        return link_list
