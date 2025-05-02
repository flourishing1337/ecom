from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price_cents = Column(Integer, nullable=False)
    image_url = Column(String)
    stock = Column(Integer, default=0)
