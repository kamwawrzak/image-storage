import boto3
from logging import Logger
from botocore.exceptions import ClientError
from typing import BinaryIO, List
from ..config import Config
from ..exceptions import S3ClientError

class S3Service:

    def __init__(self, log: Logger, config: Config):
        self.log = log
        self.s3_client = boto3.client(
            "s3",
            endpoint_url = config.aws_host,
            aws_access_key_id = config.aws_key_id,
            aws_secret_access_key = config.aws_access_key,
            region_name=config.aws_region
        )

    def create_bucket(self, name: str):
        try:
            self.s3_client.create_bucket(Bucket=name)
            self.log.debug(f"Bucket '{name}' created")
        except ClientError as e:
            raise S3ClientError(e)
    
    def upload_image(self, file: BinaryIO, bucket: str, name: str):
        try:
            file.seek(0)
            self.s3_client.upload_fileobj(file, bucket, name)

        except ClientError as e:
            raise S3ClientError(e)
        finally:
            file.close()

    def list_buckets(self) -> List[str]:
        try: 
            resp = self.s3_client.list_buckets()
            return resp["Buckets"]
        except ClientError as e:
            raise S3ClientError(e)
    
    def bucket_exists(self, bucket: str) -> bool:
        buckets = self.list_buckets()
        return True if bucket in buckets else False
