from app.database import Base
from sqlalchemy import Column, Integer, String


class Auth(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)