from datetime import date
from app.repository.models import Image


def generate_example_img(user_id: str, image_name: str) -> Image:
        img = Image(user_id, image_name)
        img.id = 1
        img.created_at = date(2024, 4, 30)
        return img
