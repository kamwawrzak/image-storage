import unittest
from unittest.mock import MagicMock
from fastapi import UploadFile
from app.service.image_service import ImageService
from .helpers import generate_example_img
from io import BytesIO

class TestImageService(unittest.TestCase):

    def setUp(self):
        self.fake_s3_host = "localhost:6767"
        self.s3_service = MagicMock()
        self.repository = MagicMock()
        self.image_service = ImageService(
            self.repository,
            self.s3_service,
            self.fake_s3_host
        )

    def test_insert_image_success(self):
        # arrange
        user_id = "user-123"
        name = "image-123.jpg"
        expected = generate_example_img(user_id, name)


        file_contents = b"Test content"
        file = BytesIO(file_contents)
        mock_upload_file = UploadFile(filename="image.jpg", file=file)

        self.s3_service.bucket_exists.return_value = False
        self.s3_service.create_bucket.return_value = None
        self.s3_service.upload_image.return_value = None
        self.repository.insert_image.return_value = expected

        # act
        actual = self.image_service.insert_image(mock_upload_file, user_id)

        # assert
        self.assertEqual(actual.img_name, expected.img_name)
        self.assertEqual(actual.id, expected.id)
        self.s3_service.bucket_exists.assert_called_once()
        self.s3_service.create_bucket.assert_called_once()
        self.s3_service.upload_image.assert_called_once()
        self.repository.insert_image.assert_called_once()

    def test_get_image_success(self):
        # arrange
        example_img = generate_example_img("user-123", "image1.jpg")
        example_img.id = "1"
        expected = "localhost:6767/user-123/image1.jpg"

        self.repository.get_image.return_value = example_img

        # act
        actual = self.image_service.get_image(example_img.user_id, example_img.id)

        # assert
        self.assertEqual(actual, expected)
        self.repository.get_image.assert_called_once_with(example_img.user_id, example_img.id)
