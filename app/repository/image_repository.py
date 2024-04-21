from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Image
from ..config import Config



class ImageRepository:

    def __init__(self, config: Config):
        db_url = self.get_dsn(config, 'mysql+pymysql')
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()
    
    def insert_image(self, user_id: str, name: str) -> Image:
        session = self.get_session()
        img = Image(user_id=user_id, img_name=name)
        try:
            session.add(img)
            session.commit()
            session.refresh(img)
            return img
        except Exception as e:
            return e
        finally:
            session.close()

    def get_image(self, user_id: str, id: str) -> Image:
        session = self.get_session()
        try:
            img = session.query(Image).filter_by(user_id=user_id, id=id).one()
            return img
        except Exception as e:
            return e
        finally:
            session.close()
    
    def get_dsn(self, config: Config, driver: str) -> str:
        user = config.db_user
        password = config.db_password
        host = config.db_host
        port = config.db_port
        database = config.db_database
        return f"{driver}://{user}:{password}@{host}:{port}/{database}"
