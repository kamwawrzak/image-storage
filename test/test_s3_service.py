import unittest
from io import BytesIO 
from unittest.mock import MagicMock
from .fake_config import FakeAWSCfg
from app.service.s3_service import S3Service

class TestS3Service(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock()
        self.s3_service = S3Service(self.logger, FakeAWSCfg())
        self.s3_service.s3_client = MagicMock()
    
    def test_create_bucket_success(self):
        # arrange
        name = "bucket-123"
        self.logger.return_value("Bucket '{name}' created")

        # act
        result = self.s3_service.create_bucket(name)

        # assert
        self.assertIsNone(result)
        self.logger.debug.assert_called_once()
    
    def test_list_buckets_success(self):
        # arrange
        mock_resp = {"Buckets": [{"Name": "bucket-123"}, {"Name": "bucket-456"}]}
        self.s3_service.s3_client.list_buckets.return_value = mock_resp
        expected = ["bucket-123", "bucket-456"]

        # act
        actual = self.s3_service.list_buckets()

        # assert
        self.assertEqual(actual, expected)
        self.s3_service.s3_client.list_buckets.assert_called_once()
    
    def test_bucket_exists(self):
        # arrange
        name = "existing-bucket"
        mock_resp = {"Buckets": [{"Name": name}]}
        self.s3_service.s3_client.list_buckets.return_value = mock_resp

        # act
        actual = self.s3_service.bucket_exists(name)

        # assert
        self.assertTrue(actual)
        self.s3_service.s3_client.list_buckets.assert_called_once()
    
    def test_upload_image(self):
        # arrange
        bucket_name = "bucket-123"
        file_name = "image-123.jpg"   
        file_contents = b"This is an example file."
        mock_file = BytesIO(file_contents)

        # act
        self.s3_service.upload_image(mock_file, bucket_name, file_name)

        # assert
        self.s3_service.s3_client.upload_fileobj.assert_called_with(mock_file, bucket_name, file_name)
        self.assertTrue(mock_file.closed)
