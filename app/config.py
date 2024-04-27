import os
import yaml
from dotenv import load_dotenv

DEFAULT_CONFIG_FILE = './config/config.local.yaml'

class Config:

    def __init__(self, config_file: str = DEFAULT_CONFIG_FILE):
        load_dotenv()
        db_password = self.get_env_var('DB_PASSWORD')
        aws_key = self.get_env_var('AWS_ACCESS_KEY_ID')
        aws_secret = self.get_env_var('AWS_SECRET_ACCESS_KEY')
        aws_host = self.get_env_var('AWS_HOST')
        db_host = self.get_env_var('DB_HOST')
        jwt_secret = self.get_env_var('JWT_SECRET')

        with open(config_file, 'r', encoding='utf-8') as file:
            cfg = yaml.safe_load(file)
            self.log_level = cfg['logger']['level']
            self.max_image_size_mb = cfg['image_service']['max_image_size_mb']
            self.allowed_extensions = cfg['image_service']['allowed_extensions']
            self.server_port = cfg['server']['port']
            self.db_host = db_host if db_host else cfg['database']['host']
            self.db_port = cfg['database']['port']
            self.db_user = cfg['database']['user']
            self.db_password =  db_password if db_password else cfg['database']['password']
            self.db_database = cfg['database']['database']
            self.aws_host = aws_host if aws_host else cfg['aws']['host']
            self.aws_region = cfg['aws']['region']
            self.aws_key_id = aws_key if aws_key else cfg['aws']['aws_access_key_id']
            self.aws_access_key = aws_secret if aws_secret else cfg['aws']['aws_secret_access_key']
            self.jwt_secret =  jwt_secret if jwt_secret else cfg['jwt']['secret']
            self.jwt_alg = cfg['jwt']['alg']

    def get_env_var(self, name: str):
        return os.environ[name]
