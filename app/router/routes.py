from fastapi import APIRouter, Depends, File, status, UploadFile
from ..service.image_service import ImageService
from ..service.auth_service import AuthService
from ..config import Config


class ImageRouter(APIRouter):

    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.image_service = ImageService(config)
        self.auth_service = AuthService(config)

        @self.post("/image", status_code=status.HTTP_201_CREATED)
        async def upload(file: UploadFile = File(...), user_id: str = Depends(self.auth_service.get_current_user)):
            ext = file.filename.split('.')[-1]
            img = await self.image_service.insert_image(file.file, user_id, ext)
            return {"image_id": img.id}

        

        @self.get("/image/{id}")
        async def get_image(id: int, user_id: str = Depends(self.auth_service.get_current_user)):
            img = self.image_service.get_image(id, user_id)
            key = img.img_name
            return {"message": 'image %s returned' % key}
