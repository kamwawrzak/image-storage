import os
import yaml
from dotenv import load_dotenv

defaultConfig = './config/config.local.yaml'

class Config:

    def __init__(self, file: str = defaultConfig):
        load_dotenv()
        db_password = self.get_env_var('DB_PASSWORD')
        aws_key = self.get_env_var('AWS_ACCESS_KEY_ID')
        aws_secret = self.get_env_var('AWS_SECRET_ACCESS_KEY')
        jwt_secret = self.get_env_var('JWT_SECRET')

        with open(file, 'r') as file:
            config = yaml.safe_load(file)
            self.max_image_size_mb = config['image_service']['max_image_size_mb']
            self.allowed_extensions = config['image_service']['allowed_extensions']
            self.server_port = config['server']['port']
            self.db_host = config['database']['host']
            self.db_port = config['database']['port']
            self.db_user = config['database']['user']
            self.db_password =  db_password if db_password else config['database']['password']
            self.db_database = config['database']['database']
            self.aws_host = config['aws']['host']
            self.aws_region = config['aws']['region']
            self.aws_key_id = aws_key if aws_key else config['aws']['aws_access_key_id']
            self.aws_access_key = aws_secret if aws_secret else config['aws']['aws_secret_access_key']
            self.jwt_secret =  jwt_secret if jwt_secret else config['jwt']['secret']
            self.jwt_alg = config['jwt']['alg']

    def get_env_var(self, name: str):
       return os.environ[name]
