from app.database import Base
from sqlalchemy import Column, Integer, String


class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True)
    nom = Column(String)