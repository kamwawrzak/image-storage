import uvicorn
from fastapi import FastAPI
from app.router.routes import ImageRouter
from app.config import Config


if __name__ == "__main__":
    config = Config()
    app = FastAPI()
    router = ImageRouter(config)
    app.include_router(router, prefix="/v1")
    uvicorn.run(uvicorn.run(app, host='0.0.0.0', port=config.server_port))
