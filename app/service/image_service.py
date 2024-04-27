import time
from fastapi import UploadFile
from ..repository.models import Image
from ..repository.image_repository import ImageRepository
from .s3_service import S3Service


class ImageService:

    def __init__(self, repository: ImageRepository, s3: S3Service, s3_host: str):
        self.s3_host = s3_host
        self.repository = repository
        self.s3_service = s3

    def insert_image(self, file: UploadFile, user_id: str) -> Image:
        name = self.get_image_name(file)
        if not self.s3_service.bucket_exists(user_id):
            self.s3_service.create_bucket(user_id)

        self.s3_service.upload_image(file.file, user_id, name)
        
        return self.repository.insert_image(user_id, name)

    def get_image(self, user_id: str, id: str) -> str:
        img = self.repository.get_image(user_id, id)
        return self.get_image_path(img)
    
    def get_image_name(self, file: UploadFile):
        ext = self.get_extension(file)
        return f'image_{int(time.time())}.{ext}'
    
    def get_extension(self, file: UploadFile) -> str:
        return file.filename.split('.')[-1]

    def get_image_path(self, image: Image) -> str:
        return f'{self.s3_host}/{image.user_id}/{image.img_name}'
