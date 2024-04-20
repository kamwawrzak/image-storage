from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Image



class ImageRepository:

    def __init__(self, db_url):
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
