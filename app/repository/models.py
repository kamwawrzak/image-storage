from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255))
    img_name = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, user_id: str, img_name: str):
        self.user_id = user_id
        self.img_name = img_name
