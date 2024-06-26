from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from .models import Image
from ..exceptions import NotFoundError, RecordAlreadyExistsError


class ImageRepository:

    def __init__(self, log: Logger, dsn: str):
        self.log = log
        self.engine = create_engine(dsn)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.session()

    def insert_image(self, user_id: str, name: str) -> Image:
        session = self.get_session()
        img = Image(user_id=user_id, img_name=name)
        try:
            session.add(img)
            session.commit()
            session.refresh(img)
            return img
        except IntegrityError as e:
            session.rollback()
            raise RecordAlreadyExistsError(e)
        finally:
            session.close()

    def get_image(self, user_id: str, img_id: str) -> Image:
        session = self.get_session()
        try:
            return session.query(Image).filter_by(user_id=user_id, id=img_id).one()
        except NoResultFound:
            self.log.info(f"Image id: '{img_id}' doesn't exist")
            raise NotFoundError
        finally:
            session.close()
