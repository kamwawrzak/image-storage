import time
from ..repository.models import Image
from ..repository.image_repository import ImageRepository
from ..config import Config
from .s3_service import S3Service
from typing import BinaryIO


class ImageService:

    def __init__(self, config: Config):
        self.database = ImageRepository(config)
        self.s3_service = S3Service(config)
        self.s3_host = config.aws_host

    async def insert_image(self, file: BinaryIO, user_id: str, ext: str) -> Image:
        name = self.get_image_name(ext)
        buckets = self.s3_service.list_buckets()
        if user_id not in buckets:
            self.s3_service.create_bucket(user_id)
        result = self.s3_service.upload_image(file, user_id, name)
        if not result:
            return False
        
        return self.database.insert_image(user_id, name)

    def get_image(self, user_id: str, id: str) -> str:
        img = self.database.get_image(user_id, id)
        return self.get_image_path(img)
    
    def get_image_name(self, ext: str):
        return f'image_{int(time.time())}.{ext}'

    def get_image_path(self, image: Image) -> str:
        return f'{self.s3_host}/{image.user_id}/{image.img_name}'
