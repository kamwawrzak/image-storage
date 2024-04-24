import unittest
from unittest.mock import MagicMock
from app.repository.image_repository import ImageRepository
from .helpers import generate_example_img


class TestImageRepository(unittest.TestCase):

    def setUp(self):
        dsn = f"mysql+pymysql://test:test@test:6543/test"
        self.repository = ImageRepository(None, dsn)
        self.repository.session = MagicMock()

    def test_insert_image_success(self):
        # arrange
        expected = generate_example_img("user1", "image1.jpg")

        self.repository.session.add(expected)
        self.repository.session.commit()
        self.repository.session.close()

        # act
        img = self.repository.insert_image(expected.user_id, expected.img_name)
        
        # assert
        self.assertEqual(img.user_id, expected.user_id)
        self.assertEqual(img.img_name, expected.img_name)
        self.repository.session.add.assert_called_once()
        self.repository.session.commit.assert_called_once()
        self.repository.session.close.assert_called_once()


    def test_get_image_success(self):
        # arrange
        expected = generate_example_img("user1", "img1.jpg")
        
        self.repository.session.return_value = self.repository.session

        mock_query = MagicMock()
        self.repository.session.query.return_value = mock_query

        mock_filter_by = MagicMock()
        mock_query.filter_by.return_value = mock_filter_by
        mock_filter_by.one.return_value = expected

        self.repository.session.close()
        
        # act
        img = self.repository.get_image(expected.user_id, expected.id)

        # assert
        self.assertEqual(img, expected)
        self.repository.session.query.assert_called_once()
        mock_query.filter_by.assert_called_once()
        mock_filter_by.one.assert_called_once()
        self.repository.session.close.assert_called()
   