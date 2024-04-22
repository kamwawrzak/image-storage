from fastapi import APIRouter, File, Request, status, UploadFile
from fastapi.responses import JSONResponse
from logging import Logger
from ..service.image_service import ImageService
from ..service.auth_service import AuthService
from ..validator.image_validator import ImageValidator
from ..config import Config
from ..exceptions import AuthenticationError, NotFoundError, RecordAlreadyExistsError, S3ClientError, ValidationError


class ImageRouter(APIRouter):

    def __init__(self, config: Config, log: Logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = log
        self.image_service = ImageService(config, log)
        self.auth_service = AuthService(config)
        self.image_validator = ImageValidator(config)

        @self.post("/image", )
        async def upload(req: Request, file: UploadFile = File(...)):
            try:
                user_id = self.auth_service.get_current_user(req)
                await self.image_validator.validate(file)
                img = await self.image_service.insert_image(file, user_id)
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"image_id": img.id}
                )
            except ValidationError as e:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"errors": e.detail}
                )
            except AuthenticationError as e:
                self.log.error(e)
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"errors": e.detail}
                )
            except RecordAlreadyExistsError:
                self.log.error(e)
                return JSONResponse(
                    status=status.HTTP_409_CONFLICT,
                    content={"errors": "record already exists"}
                )
            except S3ClientError as e:
                self.log.error(e)
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"errors": "unexpected error occurred"}
                )
        

        @self.get("/image/{id}")
        async def get_image(req: Request, id: str):
            try:
                user_id = self.auth_service.get_current_user(req)
                img = self.image_service.get_image(user_id, id)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"image_path": img}
                )
            except AuthenticationError as e:
                self.log.error(e)
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"errors": e.detail}
                )
            except S3ClientError as e:
                self.log.error(e)
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"errors": "unexpected error occurred"}
                )
            except NotFoundError:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"errors": "not found"}
                )
