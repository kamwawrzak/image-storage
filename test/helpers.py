import imghdr
from datetime import date
from unittest.mock import MagicMock
from fastapi import UploadFile
from app.repository.models import Image


def generate_example_img(user_id: str, image_name: str) -> Image:
    img = Image(user_id, image_name)
    img.id = 1
    img.created_at = date(2024, 4, 30)
    return img

def generate_mock_file(size: int, content_type: str, extension: str) -> MagicMock:
    file_mock = MagicMock(spec=UploadFile)
    file_mock.size = size
    file_mock.content_type = content_type
    imghdr.what = MagicMock(return_value=extension)
    return file_mock