if __name__ == "__main__":
    from app.config import TOKEN, VERSION, User_ID, TOKEN_YANDEX
    from app.parser import VkParser
    from app.uploader import YandexUpload

    vk_photos = VkParser(TOKEN, VERSION, User_ID, 5)
    photo_links_list = vk_photos.get_photo_links()
    upload_photo = YandexUpload()
    upload_photo.upload("file_path", TOKEN_YANDEX, photo_links_list)
