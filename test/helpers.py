from io import BytesIO
from datetime import date
from unittest.mock import MagicMock
from fastapi import UploadFile
from PIL import Image as Pil_Image
from app.repository.models import Image


def generate_example_img(user_id: str, image_name: str) -> Image:
    img = Image(user_id, image_name)
    img.id = 1
    img.created_at = date(2024, 4, 30)
    return img

def generate_mock_file(size: int, content_type: str, extension: str) -> MagicMock:
    img = Pil_Image.new('RGB', (100, 100))
    img_bytes = BytesIO()
    img.save(img_bytes, format=extension.upper())
    img_bytes.seek(0)

    file_mock = MagicMock(spec=UploadFile)
    file_mock.size = size
    file_mock.content_type = content_type
    file_mock.read.return_value = img_bytes.getvalue()

    return file_mock
