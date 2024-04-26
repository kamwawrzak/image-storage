import unittest
from unittest.mock import MagicMock
from .fake_config import FakeConfig
from app.service.s3_service import S3Service

class TestS3Service(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock()
        self.s3_service = S3Service(self.logger, FakeConfig())
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
    
    def test_bucket_exists(self):
        # arrange
        name = "existing-bucket"
        mock_resp = {"Buckets": [{"Name": name}]}
        self.s3_service.s3_client.list_buckets.return_value = mock_resp

        # act
        actual = self.s3_service.bucket_exists(name)

        # assert
        self.assertTrue(actual)
