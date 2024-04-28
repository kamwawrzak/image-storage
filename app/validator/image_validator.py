import io
from fastapi import UploadFile
from PIL import Image
from ..config import Config
from ..exceptions import ValidationError



class ImageValidator:

    def __init__(self, config: Config):
        self.max_size_mb = config.max_image_size_mb * 1024 * 1024
        self.content_type = "image/"
        self.allowed_extensions = config.allowed_extensions

    async def validate(self, file: UploadFile):
        if file.size > self.max_size_mb:
            raise ValidationError("File size exceeded")

        if not file.content_type.startswith(self.content_type):
            raise ValidationError("File is not image")

        img_data = await file.read()
        image = Image.open(io.BytesIO(img_data))
        print("tyyype: ", image.format)
        if image.format.lower() not in self.allowed_extensions:
            raise ValidationError("Unsupported image type")
