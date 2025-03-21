from sqlalchemy import Column, String, Float, Integer, Enum, JSON, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
from .pattern import Pattern
import enum

class ItemType(enum.Enum):
    WEAPON = "weapon"
    KNIFE = "knife"
    GLOVE = "glove"
    STICKER = "sticker"
    CASE = "case"
    OTHER = "other"

class Item(BaseModel):
    __tablename__ = "items"

    name = Column(String, index=True)
    type = Column(Enum(ItemType))
    market_hash_name = Column(String, unique=True, index=True)
    steam_item_id = Column(String, unique=True)
    image_url = Column(String)
    rarity = Column(String)
    collection = Column(String)
    pattern_data = Column(JSON)  # Stores pattern-specific data
    current_price = Column(Float)
    volume_24h = Column(Integer)
    last_updated = Column(DateTime)

    # Relationships
    price_history = relationship("PriceHistory", back_populates="item")
    patterns = relationship("Pattern", back_populates="item") 