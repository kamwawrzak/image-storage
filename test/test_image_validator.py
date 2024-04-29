import unittest
from app.validator.image_validator import ImageValidator
from app.exceptions import ValidationError
from .fake_config import FakeImageServiceCfg
from .helpers import generate_mock_file


class TestImageValidator(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.validator = ImageValidator(FakeImageServiceCfg())

    async def test_validate_success(self):
        # arrange
        file_mock = generate_mock_file(1024, "image/jpeg", "jpeg")

        # act
        result = await self.validator.validate(file_mock)

        # assert
        self.assertIsNone(result)
    
    async def test_validate_too_large_size(self):
        # arrange
        file_mock = generate_mock_file(10* 1024 * 1024, "image/jpeg", "jpeg")
        expectedErr = "File size exceeded"

        # act
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(file_mock)
        
        # assert
        self.assertEqual(str(context.exception), expectedErr)
    
    async def test_validate_not_image_content(self):
        # arrange
        file_mock = generate_mock_file(1024, "application/json", "jpeg")
        expectedErr = "File is not image"

        # act
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(file_mock)
        
        # assert
        self.assertEqual(str(context.exception), expectedErr)

    async def test_validate_unsupported_type(self):
        # arrange
        file_mock = generate_mock_file(1024, "image/gif", "gif")
        expectedErr = "Unsupported image type"

        # act
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(file_mock)
        
        # assert
        self.assertEqual(str(context.exception), expectedErr)
