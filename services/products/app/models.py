# app/models.py

from sqlalchemy import Column, Integer, Float, Text, Numeric
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    price       = Column(Numeric(12, 2), nullable=False)
    weight = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    name = Column(Text, nullable=False, index=True)
    discount = Column(Float, nullable=True)
    amount = Column(Integer, nullable=False)
