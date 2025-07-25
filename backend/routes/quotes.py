# Quote routes
from fastapi import APIRouter, HTTPException
from typing import List
from models import Quote, QuoteCreate, Category
from database import DatabaseManager

router = APIRouter(prefix="/quotes", tags=["quotes"])

@router.get("/{category}")
async def get_quotes_by_category(category: str, limit: int = 15):
    """Get quotes by category"""
    try:
        quotes = DatabaseManager.get_quotes_by_category(category, limit)
        return {"category": category, "quotes": quotes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quotes: {str(e)}")

@router.get("/")
async def get_all_quotes(limit: int = 100):
    """Get all quotes"""
    try:
        quotes = DatabaseManager.get_all_quotes(limit)
        return {"quotes": quotes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quotes: {str(e)}")

@router.post("/")
async def create_quote(quote_data: QuoteCreate):
    """Create a new quote"""
    try:
        new_quote = DatabaseManager.add_quote(
            quote_data.category, 
            quote_data.quote, 
            quote_data.author
        )
        return {"message": "Quote created successfully", "quote": new_quote}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating quote: {str(e)}")

@router.get("/categories/")
async def get_categories():
    """Get available quote categories"""
    try:
        return {
            "categories": [
                {"name": "motivational", "emoji": "💪", "description": "Boost your motivation and drive"},
                {"name": "romantic", "emoji": "💖", "description": "Express your love and feelings"},
                {"name": "funny", "emoji": "😂", "description": "Brighten your day with humor"},
                {"name": "inspirational", "emoji": "✨", "description": "Find hope and inspiration"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")
