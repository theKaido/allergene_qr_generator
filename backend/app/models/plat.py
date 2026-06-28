from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Plat(Base):
    __tablename__ = "plat"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    categorie = Column(String)
    id_restaurant = Column(Integer, ForeignKey("restaurant.id"))