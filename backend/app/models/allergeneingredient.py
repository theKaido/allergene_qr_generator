from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class AllergeneIngredient(Base):
    __tablename__ = "allergeneingredient"
    id_allergene = Column(Integer, ForeignKey("allergene.id"), primary_key=True)
    id_ingredient = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    status = Column(String)