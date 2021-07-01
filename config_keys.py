from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("VK_TOKEN")
TOKEN_YANDEX = os.getenv("YANDEX_TOKEN")
API_BASE_URL = "https://api.vk.com/method/"
User_ID = os.getenv("USER_ID")
V = os.getenv("VERSION")
