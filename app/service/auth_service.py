import jwt
from fastapi import Request
from ..config import JWTConfig
from ..exceptions import AuthenticationError


class AuthService:

    def __init__(self, config: JWTConfig):
        self.secret = config.secret
        self.alg = config.alg

    def get_current_user(self, req: Request) -> str:
        header = req.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            raise AuthenticationError('Missing JWT')

        token = header.split(" ")[1]
        try:
            data = jwt.decode(
                jwt=token,
                key=self.secret,
                algorithms=[self.alg]
            )
            return data['sub']
        except jwt.exceptions.InvalidTokenError as exc:
            raise AuthenticationError('Invalid JWT') from exc
