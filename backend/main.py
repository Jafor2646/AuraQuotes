# AuraQuotes Backend - FastAPI Application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import our modules
from database import init_database
from routes import init_routes

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Initialize database
    print("🚀 Starting AuraQuotes Backend...")
    print("🗄️  Initializing database...")
    init_database()
    
    # Check AI model setup
    model = os.getenv("AI_MODEL", "llama3.2:1b")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    print(f"🤖 AI Model: {model}")
    print(f"🔗 Ollama Host: {ollama_host}")
    print("✅ Agentic AI system ready!")
    
    print("✅ AuraQuotes Backend ready!")
    yield
    # Shutdown
    print("🛑 Shutting down AuraQuotes Backend...")

# Create FastAPI app
app = FastAPI(
    title="AuraQuotes API",
    description="""
    🌟 **AuraQuotes - AI-Powered Quote Platform**
    
    An intelligent quote platform with an agentic AI chatbot that uses external tools to guide users based on their mood.
    
    ## Features
    - 🤖 **Agentic AI Agent** with local LLM and external tool calling
    - 🎯 **Mood Detection** - Specialized for funny, inspirational, motivational, romantic categories
    - 🧭 **Smart Navigation** - Guides users to relevant quote categories
    - 💾 **Session Management** - Persistent chat history across interactions
    - 📱 **Multiple Categories** - Motivational, Romantic, Funny, Inspirational
    - 🛠️ **Agentic Workflow** - Tool calling architecture with separate functions
    
    ## AI Architecture
    1. **Local LLM (Llama 3.2 1B)** - Lightweight model for mood detection
    2. **External Tool System** - Agentic workflow with 6 specialized tools  
    3. **100% Free** - No API keys required, fully offline capable
    
    ## Architecture
    - **Agentic Design** - External tool calling with intelligent decision making
    - **Local Processing** - No external API dependencies
    - **Error Handling** - Comprehensive exception handling with fallbacks
    - **Type Safety** - Full Pydantic model validation
    """,
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
        "https://*.vercel.app",   # For deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize all routes
init_routes(app)

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("🌟 AuraQuotes - Agentic AI Quote System")
    print("=" * 50)
    print("📱 Frontend: http://localhost:3000")
    print("🔌 Backend API: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔄 Interactive Docs: http://localhost:8000/redoc")
    print("🤖 AI: Local LLM with external tools")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",  # Use import string for reload to work
        host="127.0.0.1", 
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
