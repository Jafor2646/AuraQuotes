# Chat routes with Agentic AI
from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse
from database import DatabaseManager
from agentic_ai import AgenticAIAgent

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize the agentic AI agent
ai_agent = AgenticAIAgent()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Agentic AI chat endpoint with full workflow capabilities
    
    Features:
    - Natural conversation with mood detection
    - Tool invocation system
    - Session management with memory
    - Emotional support
    - 100% free implementation
    """
    try:
        # Process message with enhanced agentic workflow
        ai_response = await ai_agent.process_message(request.message, request.session_id)
        
        return ChatResponse(
            response=ai_response["response"],
            session_id=ai_response["session_id"],
            tool_calls={
                "mood_analysis": ai_response["mood_analysis"],
                "tools_invoked": ai_response["tools_invoked"],
                "navigation": ai_response["tool_results"].get("quote_navigator", {}),
                "quotes_preview": ai_response["tool_results"].get("quote_fetcher", {}).get("quotes", []),
                "emotional_support": ai_response["tool_results"].get("emotional_support", {}),
                "conversation_context": ai_response["conversation_context"]
            }
        )
    
    except Exception as e:
        print(f"Chat processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

@router.get("/history/{session_id}")
async def get_chat_history_endpoint(session_id: str):
    """Get chat history for a session with enhanced context"""
    try:
        # Get from database
        history = DatabaseManager.get_chat_history(session_id)
        
        # Get from agent memory for enhanced context
        agent_context = ai_agent._get_conversation_context(session_id)
        
        return {
            "session_id": session_id, 
            "messages": history,
            "agent_context": agent_context,
            "conversation_stats": {
                "message_count": len(history),
                "mood_history": agent_context.get("mood_history", [])[-5:],  # Last 5 moods
                "created_at": agent_context.get("created_at"),
                "last_active": agent_context.get("last_active")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History retrieval error: {str(e)}")

@router.get("/sessions")
async def get_all_sessions():
    """Get all active sessions (for debugging/admin)"""
    try:
        sessions = []
        for session_id, data in ai_agent.session_memory.items():
            sessions.append({
                "session_id": session_id,
                "created_at": data.get("created_at"),
                "last_active": data.get("last_active"),
                "message_count": len(data.get("messages", [])),
                "last_mood": data.get("mood_history", [])[-1].get("primary_mood") if data.get("mood_history") else None
            })
        return {"sessions": sessions, "total_sessions": len(sessions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sessions retrieval error: {str(e)}")

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a specific session (for testing)"""
    try:
        if session_id in ai_agent.session_memory:
            del ai_agent.session_memory[session_id]
            return {"message": f"Session {session_id} cleared successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session clear error: {str(e)}")
