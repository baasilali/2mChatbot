from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class PriceHistory(BaseModel):
    __tablename__ = "price_history"

    item_id = Column(Integer, ForeignKey("items.id"))
    price = Column(Float)
    volume = Column(Integer)
    listings = Column(Integer)

    # Relationship
    item = relationship("Item", back_populates="price_history") 