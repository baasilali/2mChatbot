import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from sqlalchemy.orm import Session
from app.models.item import Item
from app.models.price_history import PriceHistory
from app.core.database import SessionLocal
import redis.asyncio as redis
import json
import logging
import re

logger = logging.getLogger(__name__)

class SteamMarketService:
    def __init__(self):
        self.api_key = os.getenv("STEAM_API_KEY")
        self.base_url = "https://api.steampowered.com/ISteamEconomy"
        self.headers = {
            "key": self.api_key,
            "Accept": "application/json"
        }
        self.redis = redis.from_url("redis://redis:6379")
        self.cache_ttl = 300  # 5 minutes cache
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    async def get_cached_price(self, market_hash_name: str) -> Optional[Dict]:
        try:
            cached = await self.redis.get(f"price:{market_hash_name}")
            if cached:
                data = json.loads(cached)
                data["source"] = "cache"
                return data
        except Exception as e:
            logger.error(f"Cache error for {market_hash_name}: {str(e)}")
        return None

    async def set_cached_price(self, market_hash_name: str, price_data: Dict):
        try:
            await self.redis.setex(
                f"price:{market_hash_name}",
                timedelta(seconds=self.cache_ttl),
                json.dumps(price_data)
            )
        except Exception as e:
            logger.error(f"Failed to cache price for {market_hash_name}: {str(e)}")

    async def fetch_listings_count(self, session: aiohttp.ClientSession, market_hash_name: str) -> Optional[int]:
        """Fetch the actual number of listings from Steam's market page."""
        url = f"https://steamcommunity.com/market/listings/730/{market_hash_name}"
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    # Look for the listings count in the page
                    match = re.search(r'Showing (\d+) listings', html)
                    if match:
                        return int(match.group(1))
                return 0
        except Exception as e:
            logger.error(f"Error fetching listings count for {market_hash_name}: {str(e)}")
            return 0

    async def fetch_from_steam(self, session: aiohttp.ClientSession, market_hash_name: str) -> Optional[Dict]:
        """Make actual API call to Steam with retries."""
        url = "https://steamcommunity.com/market/priceoverview/"
        params = {
            "currency": 1,
            "appid": 730,
            "market_hash_name": market_hash_name
        }

        for attempt in range(self.max_retries):
            try:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            # Fetch actual listings count
                            listings = await self.fetch_listings_count(session, market_hash_name)
                            return {
                                "price": float(data.get("lowest_price", "0").replace("$", "").strip()),
                                "volume": int(data.get("volume", "0").replace(",", "")),
                                "listings": listings,
                                "source": "api",
                                "timestamp": datetime.utcnow().isoformat()
                            }
                    elif response.status == 429:  # Rate limit
                        wait_time = 5 * (attempt + 1)  # Progressive backoff
                        logger.warning(f"Rate limited, waiting {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Steam API error: Status {response.status}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Request timeout, attempt {attempt + 1}/{self.max_retries}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
            
            if attempt < self.max_retries - 1:  # Don't sleep on last attempt
                await asyncio.sleep(self.retry_delay * (attempt + 1))
        
        return None

    async def fetch_item_price(self, market_hash_name: str) -> Optional[Dict]:
        """Main method to fetch price with caching and error handling."""
        try:
            # Try cache first
            cached_price = await self.get_cached_price(market_hash_name)
            if cached_price:
                return cached_price

            # If not in cache, fetch from Steam
            async with aiohttp.ClientSession() as session:
                price_data = await self.fetch_from_steam(session, market_hash_name)
                
                if price_data:
                    # Cache successful response
                    await self.set_cached_price(market_hash_name, price_data)
                    return price_data
                else:
                    # If Steam API fails, return stale cache if available
                    stale_cache = await self.redis.get(f"price:{market_hash_name}")
                    if stale_cache:
                        data = json.loads(stale_cache)
                        data["source"] = "stale_cache"
                        return data
                    
                    return {"error": "Price unavailable", "source": "error"}

        except Exception as e:
            logger.error(f"Error fetching price for {market_hash_name}: {str(e)}")
            return {"error": str(e), "source": "error"}

    async def update_item_prices(self):
        """Update prices for all items in the database."""
        db = SessionLocal()
        try:
            items = db.query(Item).all()
            for item in items:
                price_data = await self.fetch_item_price(item.market_hash_name)
                if price_data:
                    # Update item
                    item.current_price = float(price_data["price"])
                    item.volume_24h = price_data["volume"]
                    item.last_updated = datetime.utcnow()

                    # Create price history entry
                    price_history = PriceHistory(
                        item_id=item.id,
                        price=float(price_data["price"]),
                        volume=price_data["volume"],
                        listings=price_data["listings"]
                    )
                    db.add(price_history)
            
            db.commit()
        finally:
            db.close()

    async def start_price_updates(self):
        """Start the price update loop."""
        while True:
            await self.update_item_prices()
            await asyncio.sleep(int(os.getenv("STEAM_MARKET_UPDATE_INTERVAL", 300))) 