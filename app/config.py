from pathlib import Path

from dotenv import load_dotenv
import os


BASE_DIR = Path().resolve()

load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("VK_TOKEN")
TOKEN_YANDEX = os.getenv("YANDEX_TOKEN")
API_BASE_URL = "https://api.vk.com/method/"
User_ID = os.getenv("USER_ID_VK")
VERSION = os.getenv("VERSION", 5.107)
