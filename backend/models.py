# Backend Models
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    tool_calls: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    tool_calls: Optional[Dict[str, Any]] = None

class Quote(BaseModel):
    id: int
    category: str
    quote: str
    author: str
    created_at: str

class QuoteCreate(BaseModel):
    category: str
    quote: str
    author: str

class Category(BaseModel):
    name: str
    emoji: str
    description: str

class SessionResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]

class IntentResult(BaseModel):
    intent: str
    confidence: float
    suggested_category: str

class NavigationResult(BaseModel):
    action: str
    page: str
    category: str
    message: str
