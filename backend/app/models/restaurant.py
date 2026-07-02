from app.database import Base
from sqlalchemy import Integer, Column, ForeignKey, String


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie = Column(String)
    auth_id = Column(Integer, ForeignKey("auth.id"), nullable=False)