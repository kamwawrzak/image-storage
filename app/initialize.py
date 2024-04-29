from logging import Logger
from app.router.routes import ImageRouter
from app.repository.image_repository import ImageRepository
from app.service.auth_service import AuthService
from app.service.s3_service import S3Service
from app.service.image_service import ImageService
from app.validator.image_validator import ImageValidator
from app.config import Config, DatabaseConfig


def initialize(log: Logger, config: Config) -> ImageRouter:
    dsn = get_dsn(config.db, 'mysql+pymysql')
    repository = ImageRepository(log, dsn)
    s3_service = S3Service(log, config.aws)
    auth_service = AuthService(config.jwt)
    validator = ImageValidator(config.image_service)
    img_service = ImageService(repository, s3_service, config.aws.host)

    return ImageRouter(log, auth_service, validator, img_service)

def get_dsn(config: DatabaseConfig, driver: str) -> str:
    user = config.user
    password = config.password
    host = config.host
    port = config.port
    database = config.database

    return f"{driver}://{user}:{password}@{host}:{port}/{database}"
