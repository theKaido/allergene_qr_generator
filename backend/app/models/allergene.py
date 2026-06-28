from app.database import Base
from sqlalchemy import Column, Integer, String


class Allergene(Base):
    __tablename__ = "allergene"
    id = Column(Integer, primary_key=True)
    nom = Column(String)    