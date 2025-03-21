from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.item import Item, ItemType
from datetime import datetime

def init_items():
    db = SessionLocal()
    try:
        # Basic CS2 items to track
        items = [
            Item(
                name="AK-47 | Asiimov",
                type=ItemType.WEAPON,
                market_hash_name="AK-47 | Asiimov (Factory New)",
                steam_item_id="730_2_1",
                image_url="https://steamcommunity-a.akamaihd.net/economy/image/...",
                rarity="Covert",
                collection="Operation Phoenix",
                current_price=0.0,
                volume_24h=0,
                last_updated=datetime.utcnow()
            ),
            Item(
                name="M4A4 | Howl",
                type=ItemType.WEAPON,
                market_hash_name="M4A4 | Howl (Factory New)",
                steam_item_id="730_2_2",
                image_url="https://steamcommunity-a.akamaihd.net/economy/image/...",
                rarity="Contraband",
                collection="Operation Bravo",
                current_price=0.0,
                volume_24h=0,
                last_updated=datetime.utcnow()
            ),
            # Add more items as needed
        ]

        for item in items:
            db.add(item)
        
        db.commit()
        print("Successfully initialized items")
    except Exception as e:
        print(f"Error initializing items: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_items() 