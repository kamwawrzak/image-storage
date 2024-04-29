import os
from typing import Optional, Dict, Any
import yaml
from dotenv import load_dotenv


DEFAULT_CONFIG_FILE = './config/config.local.yaml'

class DatabaseConfig:
    def __init__(self, config: Dict[str, Any]):
        self.host = os.getenv('DB_HOST') or config.get('host')
        self.port = config.get('port')
        self.user = config.get('user')
        self.password = os.getenv('DB_PASSWORD') or config.get('password')
        self.database = config.get('database')

class AWSConfig:
    def __init__(self, config: Dict[str, Any]):
        self.host = os.getenv('AWS_HOST') or config.get('host')
        self.region = config.get('region')
        self.access_key_id = os.getenv('AWS_ACCESS_KEY_ID') or \
            config.get('aws_access_key_id')
        self.secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY') or \
            config.get('aws_secret_access_key')

class ServerConfig:
    def __init__(self, config: Dict[str, Any]):
        self.port = config.get('port')

class ImageServiceConfig:
    def __init__(self, config: Dict[str, Any]):
        self.max_image_size_mb = config.get('max_image_size_mb')
        self.allowed_extensions = config.get('allowed_extensions')

class JWTConfig:
    def __init__(self, config: Dict[str, Any]):
        self.secret = os.getenv('JWT_SECRET') or config.get('secret')
        self.alg = config.get('alg')

class Config:
    def __init__(self, config_file: Optional[str] = None):
        load_dotenv()

        if config_file is None:
            config_file = os.getenv('CONFIG_FILE_PATH', DEFAULT_CONFIG_FILE)

        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                cfg = yaml.safe_load(file)
        except FileNotFoundError:
            raise RuntimeError(f"Config file not found: {config_file}")
        except yaml.YAMLError:
            raise RuntimeError(f"Error parsing YAML file: {config_file}")


        self.db = DatabaseConfig(cfg.get('database'))
        self.aws = AWSConfig(cfg.get('aws'))

        self.server = ServerConfig(cfg.get('server'))
        self.image_service = ImageServiceConfig(cfg.get('image_service'))
        self.jwt = JWTConfig(cfg.get('jwt'))
        self.log_level = cfg.get('logger').get('level')
