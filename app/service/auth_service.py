import jwt
from fastapi import HTTPException, Request, status
from ..config import Config


class AuthService:


    def __init__(self, config: Config):
        self.secret = config.jwt_secret
        pass

    def get_current_user(self, req: Request) -> str:
        header = req.headers.get("Authorization")
    
        if not header or not header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
        token = header.split(" ")[1]
    
        try:
            data  = jwt.decode(jwt=token,
                              key=self.secret,
                              algorithms=["HS256"])
            return data['sub']
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
