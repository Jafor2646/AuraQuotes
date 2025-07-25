# Routes initialization
from fastapi import APIRouter
from . import chat, quotes

def init_routes(app):
    """Initialize all routes"""
    app.include_router(chat.router)
    app.include_router(quotes.router)
    
    # Health check route
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to AuraQuotes API",
            "version": "2.0.0",
            "ai_models": ["OpenAI GPT-3.5", "Hugging Face BART", "Rule-based fallback"],
            "endpoints": {
                "chat": "/chat/",
                "quotes": "/quotes/",
                "categories": "/quotes/categories/",
                "docs": "/docs"
            }
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "AuraQuotes API"}
