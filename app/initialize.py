from logging import Logger
from app.router.routes import ImageRouter
from app.repository.image_repository import ImageRepository
from app.service.auth_service import AuthService
from app.service.s3_service import S3Service
from app.service.image_service import ImageService
from app.validator.image_validator import ImageValidator
from app.config import Config


def initialize(log: Logger, config: Config) -> ImageRouter:
    dsn = get_dsn(config, 'mysql+pymysql')
    repository = ImageRepository(log, dsn)
    s3_service = S3Service(log, config)
    auth_service = AuthService(config)
    validator = ImageValidator(config)
    img_service = ImageService(repository, s3_service, config.aws_host)
    
    return ImageRouter(log, auth_service, validator, img_service)

def get_dsn(config: Config, driver: str) -> str:
        user = config.db_user
        password = config.db_password
        host = config.db_host
        port = config.db_port
        database = config.db_database
        return f"{driver}://{user}:{password}@{host}:{port}/{database}"
