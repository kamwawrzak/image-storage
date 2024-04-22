import time
from fastapi import UploadFile
from logging import Logger
from ..repository.models import Image
from ..repository.image_repository import ImageRepository
from ..config import Config
from .s3_service import S3Service


class ImageService:

    def __init__(self, config: Config, log: Logger):
        self.log = log
        self.database = ImageRepository(config, log)
        self.s3_service = S3Service(config, log)
        self.s3_host = config.aws_host

    async def insert_image(self, file: UploadFile, user_id: str) -> Image:
        name = self.get_image_name(file)
        if not self.s3_service.bucket_exists(user_id):
            self.s3_service.create_bucket(user_id)

        self.s3_service.upload_image(file.file, user_id, name)
        self.log.debug(f"Upload image '{name}' to bucket '{user_id}'")

        return self.database.insert_image(user_id, name)

    def get_image(self, user_id: str, id: str) -> str:
        img = self.database.get_image(user_id, id)
        return self.get_image_path(img)
    
    def get_image_name(self, file: UploadFile):
        ext = self.get_extension(file)
        return f'image_{int(time.time())}.{ext}'
    
    def get_extension(self, file: UploadFile) -> str:
        return file.filename.split('.')[-1]

    def get_image_path(self, image: Image) -> str:
        return f'{self.s3_host}/{image.user_id}/{image.img_name}'
