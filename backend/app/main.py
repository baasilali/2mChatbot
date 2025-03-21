from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.steam_market import SteamMarketService
from pydantic import BaseModel
import asyncio
import logging

app = FastAPI(title="CS2 Trading Bot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Steam Market Service
steam_service = SteamMarketService()

# Add logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup."""
    asyncio.create_task(steam_service.start_price_updates())

@app.get("/")
async def root():
    return {"message": "Welcome to CS2 Trading Bot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/items/{market_hash_name}/price")
async def get_item_price(market_hash_name: str):
    """Get current price for a specific item."""
    logger.info(f"Fetching price for: {market_hash_name}")
    price_data = await steam_service.fetch_item_price(market_hash_name)
    if price_data:
        return price_data
    logger.error(f"Failed to fetch price for: {market_hash_name}")
    raise HTTPException(status_code=404, detail="Item not found or price unavailable")

@app.post("/chat")
async def chat(message: ChatMessage):
    """Handle chat messages."""
    # Simple response for now
    return {
        "message": "I understand you're asking about CS2 items. Please try asking about specific item prices, patterns, or market trends."
    } 