import time
from ..repository.models import Image
from ..repository.image_repository import ImageRepository
from.. config import Config
from .s3_uploader import S3Uploader
from typing import BinaryIO


class ImageService:

    def __init__(self, config: Config):
        self.database = ImageRepository(self.get_dsn(config, 'mysql+pymysql'))
        self.db = self.database.get_session()
        self.cloud_provider = S3Uploader(config)

    async def insert_image(self, file: BinaryIO, user_id: str, ext: str) -> Image:
        name = self.get_image_name(ext)
        buckets = self.cloud_provider.list_buckets()
        if user_id not in buckets:
            self.cloud_provider.create_bucket(user_id)
        result = self.cloud_provider.upload_image(file, user_id, name)
        if not result:
            return False
        
        return self.database.insert_image(user_id, name)


    def get_image(self, id: int, user_id: int) -> Image:
        img = self.db.query(Image).filter_by(user_id=user_id, id=id).one()
        return img

    def get_dsn(self, config: Config, driver: str) -> str:
        user = config.db_user
        password = config.db_password
        host = config.db_host
        port = config.db_port
        database = config.db_database
        return f"{driver}://{user}:{password}@{host}:{port}/{database}"
    
    def get_image_name(self, ext: str):
        return f'image_{int(time.time())}.{ext}'
