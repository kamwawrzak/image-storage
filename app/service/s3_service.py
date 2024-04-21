import boto3
import io
from botocore.exceptions import ClientError
from typing import BinaryIO, List
from ..config import Config

class S3Service:

    def __init__(self, config: Config):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url = config.aws_host,
            aws_access_key_id = config.aws_key_id,
            aws_secret_access_key = config.aws_access_key,
        )

    def create_bucket(self, name: str) -> bool:
        try:
            self.s3_client.create_bucket(Bucket=name) 
        except ClientError as e:
            return False
        return True
    
    def upload_image(self, file: BinaryIO, bucket: str, name: str) -> bool:
        try: 
            contents = file.read()
            temp_file = io.BytesIO()
            temp_file.write(contents)
            temp_file.seek(0)
            self.s3_client.upload_fileobj(temp_file, bucket, name)
            return True
        except ClientError:
            return False
        finally:
            temp_file.close()


    def list_buckets(self) -> List[str]:
        resp = resp = self.s3_client.list_buckets()
        return resp["Buckets"]
