# 🌟 AuraQuotes - AI-Powered Quote Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange.svg)](https://ollama.com)

AuraQuotes is an intelligent quote platform featuring an **agentic AI chatbot** that uses local LLM technology and external tool calling to provide personalized quote recommendations based on user mood detection.

## 🎯 Key Features

- **🤖 Agentic AI Agent**: Advanced chatbot with external tool calling capabilities (similar to OpenAI function calling)
- **🎭 Smart Mood Detection**: Specialized detection for motivational, romantic, funny, and inspirational moods
- **🧭 Intelligent Navigation**: AI guides users to relevant quote categories based on emotional state
- **💾 Session Management**: Persistent conversation history and context awareness
- **🔒 100% Privacy-First**: All AI processing happens locally using Ollama
- **💰 Completely Free**: No API keys or subscriptions required
- **🛠️ External Tools**: 6 specialized tools for mood analysis, quote fetching, navigation, and emotional support

## �️ Architecture

### Backend (FastAPI)
- **Agentic AI System**: Local LLM with tool calling workflow
- **Database**: SQLite with 100+ categorized quotes
- **API Endpoints**: RESTful APIs for chat and quote management
- **Session Management**: Persistent user state tracking

### Frontend (Next.js)
- **Modern React UI**: Responsive design with Tailwind CSS
- **Real-time Chat**: Interactive conversation interface
- **Quote Categories**: Organized browsing experience
- **Mobile Responsive**: Works seamlessly on all devices

### AI Engine (Ollama + Llama 3.2)
- **Local LLM**: Llama 3.2 1B model for privacy and speed
- **Tool Calling**: 6 external tools for specialized functions
- **Context Awareness**: Multi-turn conversation understanding
- **Mood Classification**: Advanced emotion detection algorithms

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Node.js 18+**
3. **Ollama** (for local LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jafor2646/AuraQuotes.git
   cd AuraQuotes
   ```

2. **Install Ollama and download the AI model**
   ```bash
   # Install Ollama from https://ollama.com/download
   # Then download the model:
   ollama pull llama3.2:1b
   ```

3. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Create environment file
   cp .env.example .env
   # Edit .env if needed (default settings work for most setups)
   ```

4. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

#### Option 1: Run everything from project root (Recommended)
```bash
# From the project root directory
python main.py
```

This will start the backend server at `http://localhost:8000`

#### Option 2: Run backend and frontend separately
```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

Create `.env` file in the backend directory:

```env
# AI Model Configuration
AI_MODEL=llama3.2:1b
OLLAMA_HOST=http://localhost:11434

# Database Configuration  
DATABASE_URL=sqlite:///./database.db

# Server Configuration
DEBUG=True
```

### AI Model Options

| Model | Size | Speed | Quality | Recommended For |
|-------|------|-------|---------|----------------|
| `llama3.2:1b` | 1.3GB | Fast | Good | Development, testing |
| `llama3.2:3b` | 2.0GB | Medium | Better | Production |
| `llama3.1:8b` | 4.7GB | Slower | Best | High-quality responses |

To change models:
```bash
ollama pull llama3.2:3b
# Update AI_MODEL in .env file
```

## 🛠️ Agentic AI System

AuraQuotes features a sophisticated agentic AI architecture with 6 specialized external tools:

### 1. **Mood Analyzer** 🎭
- Advanced emotion detection using LLM and pattern matching
- Supports: motivational, romantic, funny, inspirational, general
- Provides confidence scores and emotional intensity metrics

### 2. **Quote Navigator** 🧭
- Intelligent routing to relevant quote categories
- Context-aware page recommendations
- Confidence-based decision making

### 3. **Quote Fetcher** 📚
- Contextual quote retrieval from database
- Quality-based ranking algorithm
- Category-specific filtering

### 4. **Conversation Manager** 💬
- Multi-turn dialogue management
- Context preservation across sessions
- Conversation flow optimization

### 5. **Session Manager** 💾
- Persistent user state tracking
- Memory management and cleanup
- Cross-session continuity

### 6. **Emotional Support** 🤗
- Contextual empathy and encouragement
- Intensity-based response adaptation
- Crisis detection and appropriate support

## 📡 API Endpoints

### Chat Endpoints
- `POST /chat/` - Main chat interface with agentic AI
- `GET /chat/history/{session_id}` - Retrieve conversation history

### Quote Endpoints
- `GET /quotes/` - List all quotes with pagination
- `GET /quotes/categories/` - List available categories
- `GET /quotes/category/{category}` - Get quotes by category
- `GET /quotes/{quote_id}` - Get specific quote

### System Endpoints
- `GET /` - API welcome and information
- `GET /health` - Health check endpoint

## 🗄️ Database Schema

### Quotes Table
```sql
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY,
    quote TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions Table
```sql
CREATE TABLE chat_sessions (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions (id)
);
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Test the AI system
python -c "
import asyncio
from agentic_ai import AgenticAIAgent

async def test():
    agent = AgenticAIAgent()
    result = await agent.process_message('I need motivation for my goals')
    print(result['response'])

asyncio.run(test())
"
```

### API Testing
```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"message": "I feel sad and need some motivation", "user_id": "test_user"}'

# Test quotes endpoint
curl "http://localhost:8000/quotes/category/motivational"
```

## 🔒 Privacy & Security

- **🏠 Local Processing**: All AI operations run locally on your machine
- **🔐 No External APIs**: No data sent to third-party services
- **💰 Zero Cost**: No API keys or subscriptions required
- **🕶️ Private Conversations**: Chat history stays on your device
- **🗄️ Local Database**: All data stored in local SQLite database

## � Troubleshooting

### Common Issues

1. **Ollama not found**
   ```bash
   # Install Ollama from https://ollama.com/download
   # Verify installation
   ollama --version
   ```

2. **Model not downloaded**
   ```bash
   ollama pull llama3.2:1b
   ollama list  # Verify model is downloaded
   ```

3. **Backend startup errors**
   ```bash
   cd backend
   pip install -r requirements.txt  # Reinstall dependencies
   python -m uvicorn main:app --reload  # Try direct startup
   ```

4. **Frontend not connecting to backend**
   - Check backend is running on port 8000
   - Verify CORS settings in backend/main.py
   - Check network connectivity

### Performance Optimization

1. **For faster responses**: Use `llama3.2:1b` model
2. **For better quality**: Use `llama3.2:3b` or larger models  
3. **Memory issues**: Restart Ollama service
4. **Database performance**: Regular cleanup of old sessions

## 🔄 Development

### Project Structure
```
AuraQuotes/
├── main.py                 # Main application entry point
├── README.md               # This documentation
├── backend/
│   ├── main.py            # FastAPI application
│   ├── agentic_ai.py      # AI agent with tool calling
│   ├── database.py        # Database operations
│   ├── models.py          # Pydantic models
│   ├── requirements.txt   # Python dependencies
│   └── routes/
│       ├── chat.py        # Chat endpoints
│       └── quotes.py      # Quote endpoints
├── frontend/
│   ├── package.json       # Node.js dependencies
│   ├── src/
│   └── public/
└── ...
```

### Adding New Features

1. **New Quote Categories**: Add to database and update mood patterns
2. **Additional Tools**: Extend the agentic AI system with new external tools
3. **Enhanced UI**: Modify frontend components in the src directory
4. **Custom Models**: Train or fine-tune models for specific use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🌟 Acknowledgments

- **Ollama** for providing excellent local LLM infrastructure
- **Meta** for the Llama models
- **FastAPI** for the robust backend framework
- **Next.js** for the modern frontend framework
- **The open-source community** for making this possible

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/Jafor2646/AuraQuotes/issues)
3. Create a new issue with detailed information
4. Join our community discussions

---

**Made with ❤️ using 100% free and open-source technologies**

