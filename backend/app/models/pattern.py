from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Pattern(BaseModel):
    __tablename__ = "patterns"

    name = Column(String)
    description = Column(String)
    tier = Column(String)  # e.g., "Tier 1", "Tier 2", etc.
    pattern_id = Column(Integer)  # Steam pattern ID
    wear_range = Column(JSON)  # Min and max wear values
    rarity = Column(String)
    estimated_value = Column(Integer)
    market_hash_name = Column(String, ForeignKey("items.market_hash_name"))
    
    # Relationship
    item = relationship("Item", back_populates="patterns") 