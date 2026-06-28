from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey


class PlatIngredient(Base):
    __tablename__ = "platingredient"
    id_plat = Column(Integer, ForeignKey("plat.id"), primary_key=True)
    id_ingredient = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    