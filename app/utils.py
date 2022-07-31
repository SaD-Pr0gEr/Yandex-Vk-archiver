import requests
from alive_progress import alive_bar


def choose_biggest_size(sizes):
    size = "smxopqryzw"
    return max(sizes, key=lambda s: size.index(s["type"]))


def progress_bar(func):
    def wrapper(**kwargs):
        print("Uploading... Please wait!")
        with alive_bar(len(kwargs["data"])) as bar:
            func(bar=bar, **kwargs)
    return wrapper


class RequestManager:
    """Менеджер работы с requests"""

    def get(self, link: str, headers: dict = None, params: dict = None):
        return requests.get(link, headers=headers if headers else {"User-Agent": "Parser"}, params=params)

    def post(self, link: str, headers: dict = None, params: dict = None):
        return requests.post(link, headers=headers if headers else {"User-Agent": "Uploader"}, params=params)

    def patch(self, link: str, headers: dict = None, params: dict = None):
        pass

    def put(self, link: str, headers: dict = None, params: dict = None):
        pass

    def delete(self, link: str, headers: dict = None, params: dict = None):
        pass
