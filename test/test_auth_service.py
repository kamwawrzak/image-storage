import jwt
import unittest
from unittest.mock import MagicMock
from app.service.auth_service import AuthService
from app.exceptions import AuthenticationError


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.config = TestAuthConfig()
        self.auth_service = AuthService(config=TestAuthConfig)

    def test_get_current_user_success(self):
        # arrange
        expected = "user1"
        token = jwt.encode({"sub": expected}, self.config.jwt_secret, algorithm=self.config.jwt_alg)
        req = MagicMock()
        req.headers = {"Authorization": f"Bearer {token}"}


        # act
        actual = self.auth_service.get_current_user(req)

        # assert
        self.assertEqual(actual, expected)
    
    def test_get_current_user_missing_jwt(self):
        # arrange
        req = MagicMock()
        req.headers = {}


        # act
        with self.assertRaises(AuthenticationError) as context:
            self.auth_service.get_current_user(req)

        # assert
        self.assertEqual(str(context.exception), "Missing JWT")
    
    def test_get_current_user_invalid_jwt(self):
        # arrange
        req = MagicMock()
        req.headers = {"Authorization": f"Bearer invalid-jwt"}


        # act
        with self.assertRaises(AuthenticationError) as context:
            self.auth_service.get_current_user(req)

        # assert
        self.assertEqual(str(context.exception), "Invalid JWT")

class TestAuthConfig:
    jwt_secret="secret-123"
    jwt_alg="HS256"
