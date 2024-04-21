from fastapi import UploadFile, HTTPException, status
import imghdr
from ..config import Config



class ImageValidator:

    def __init__(self, config: Config):
        self.max_size_mb = config.max_image_size_mb * 1024 * 1024
        self.content_type = "image/"
        self.allowed_extensions = config.allowed_extensions

    async def validate(self, file: UploadFile):
        if file.size > self.max_size_mb:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeded")
        
        if not file.content_type.startswith(self.content_type):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not image")
        
        file_contents = await file.read()
        if imghdr.what(None, file_contents) not in self.allowed_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")   
