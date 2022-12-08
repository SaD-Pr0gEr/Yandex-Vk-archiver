from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path().resolve().parent


@dataclass
class YandexConfig:
    CLIENT_ID: str
    APPLICATION_SECRET: str


@dataclass
class VkConfig:
    TOKEN: str
    USER_ID: int
    API_VERSION: int


@dataclass
class AppConfig:
    YANDEX_CONFIG: YandexConfig
    VK_CONFIG: VkConfig


def load_config(env_file_path: str) -> AppConfig:
    load_dotenv(env_file_path)
    VK_TOKEN = os.getenv("VK_TOKEN")
    VK_USER_ID = int(os.getenv("USER_ID_VK"))
    VK_API_VERSION = int(os.getenv("VERSION", 5.107))
    YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
    YANDEX_APP_SECRET = os.getenv("YANDEX_CLIENT_ID")
    return AppConfig(
        YandexConfig(YANDEX_CLIENT_ID, YANDEX_APP_SECRET),
        VkConfig(VK_TOKEN, VK_USER_ID, VK_API_VERSION)
    )
