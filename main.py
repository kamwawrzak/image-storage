import uvicorn
from fastapi import FastAPI
from app.config import Config
from app.logger import get_logger
from app.initialize import initialize




if __name__ == "__main__":
    config = Config()
    log = get_logger(config)


    router = initialize(log, config)
    app = FastAPI()
    app.include_router(router, prefix="/v1")
    uvicorn.run(uvicorn.run(app, host='0.0.0.0', port=config.server_port))
