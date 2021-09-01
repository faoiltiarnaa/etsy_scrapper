from sqlalchemy import Column, String, Integer, REAL
from database import Base


class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True)
    title = Column(String(150))
    price = Column(REAL)
    currency = Column(String(5))
    image = Column(String)

    def __init__(self, product_id, title, price, currency, image):
        self.product_id = product_id
        self.title = title
        self.price = price
        self.currency = currency
        self.image = image

    def __repr__(self):
        return f"Product({self.product_id})"

    def __str__(self):
        return f"{self.product_id} | {self.title} | {self.price} {self.currency} |  {self.image}"
