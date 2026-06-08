from sqlalchemy import Column, String, Float, Boolean
from database import Base

class Product(Base):

    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    in_stock = Column(Boolean)