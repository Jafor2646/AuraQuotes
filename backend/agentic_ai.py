# Agentic AI Agent with Lightweight LLM - Free Implementation
import os
import json
import asyncio
import re
import random
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import uuid
import ollama
from database import DatabaseManager
from rag_system import EnhancedRAGAgent

class Tool:
    """Base class for external tools used by the AI agent"""
    def __init__(self, name: str, description: str, func: Callable, parameters: Dict[str, Any] = None):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}

class AgenticAIAgent:
    """
    Advanced Agentic AI Agent with external tool calling capabilities.
    
    Features:
    - Lightweight LLM for natural language understanding
    - External tool invocation system (function calling style)
    - Mood detection specialized for: funny, inspirational, motivational, romantic
    - Session management with conversation memory
    - Enhanced RAG system with vector embeddings and 100+ training prompts
    - 100% free using local Ollama LLM
    """
    
    def __init__(self):
        self.model = os.getenv("AI_MODEL", "llama3.2:1b")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        
        # Performance settings with hybrid mode for optimal speed + accuracy
        fast_mode_setting = os.getenv("AI_FAST_MODE", "hybrid").lower()
        self.fast_mode = fast_mode_setting == "true"
        self.hybrid_mode = fast_mode_setting == "hybrid"
        
        # Session and memory management
        self.session_memory = {}
        self.user_states = {}
        
        # Initialize Enhanced RAG System
        self.rag_agent = EnhancedRAGAgent()
        self.rag_initialized = False
        
        # Initialize external tools for agentic workflow
        self.tools = self._initialize_external_tools()
        
        # Conversation templates
        self.conversation_templates = self._initialize_conversation_templates()
        
        if self.hybrid_mode:
            mode_text = "Hybrid Mode (5-10s, High Accuracy)"
        elif self.fast_mode:
            mode_text = "Fast Mode (<1s, Good Accuracy)"  
        else:
            mode_text = "Full Mode (10-30s, Max Accuracy)"
        print(f"🤖 AgenticAIAgent initialized with {self.model} - {mode_text} ready!")
        
    def _initialize_external_tools(self) -> Dict[str, Tool]:
        """Initialize external tools that the agent can invoke"""
        return {
            "mood_analyzer": Tool(
                name="mood_analyzer",
                description="Analyzes user emotional state to detect mood category: funny, inspirational, motivational, romantic, or general",
                func=self.analyze_mood_with_llm,
                parameters={"input": "string", "context": "object"}
            ),
            "quote_navigator": Tool(
                name="quote_navigator", 
                description="Returns appropriate quote page URL based on detected mood category",
                func=self.navigate_to_quotes,
                parameters={"mood": "string", "confidence": "number"}
            ),
            "quote_fetcher": Tool(
                name="quote_fetcher",
                description="Fetches relevant quotes from database based on mood category",
                func=self.fetch_relevant_quotes,
                parameters={"category": "string", "count": "number"}
            ),
            "conversation_manager": Tool(
                name="conversation_manager",
                description="Manages conversation flow, context, and user engagement",
                func=self.manage_conversation_flow,
                parameters={"message": "string", "session_id": "string", "history": "array"}
            ),
            "session_manager": Tool(
                name="session_manager", 
                description="Handles session creation, memory management, and user state tracking",
                func=self.manage_user_session,
                parameters={"session_id": "string", "action": "string"}
            ),
            "emotional_support": Tool(
                name="emotional_support",
                description="Provides contextual emotional support and encouragement based on user needs",
                func=self.provide_emotional_support,
                parameters={"mood": "string", "intensity": "number", "context": "object"}
            )
        }
        
    def _initialize_conversation_templates(self) -> Dict[str, Any]:
        """Templates for natural conversation responses"""
        return {
            "greeting_responses": [
                "Hello! I'm your AI companion specializing in mood-based quote recommendations. How are you feeling today?",
                "Hi there! I'm here to understand your emotional state and find perfect quotes for your mood. What's on your mind?",
                "Welcome! I'm an AI agent that detects your mood and provides personalized quote experiences. How can I help you today?"
            ],
            "mood_acknowledgments": {
                "motivational": [
                    "I can sense you're looking for some motivation and drive! Let me find quotes that will energize and inspire you.",
                    "Motivation is what you need right now - I'll help you find that inner fire with the perfect quotes."
                ],
                "romantic": [
                    "I detect romantic feelings or needs in your message. Love and connection are beautiful - let me find quotes that speak to your heart.",
                    "Romance is in the air! Whether it's celebration or longing, I'll find quotes that capture those heart feelings."
                ],
                "funny": [
                    "You're in need of some humor and laughter! Life's better with a smile - let me find quotes that will brighten your day.",
                    "I can tell you want something funny and uplifting. Laughter is the best medicine - here come some cheerful quotes!"
                ],
                "inspirational": [
                    "I sense you're seeking deeper meaning and inspiration. That's beautiful - let me find quotes that will uplift your spirit.",
                    "Looking for inspiration and wisdom, I see. Let me find quotes that will guide and encourage your journey."
                ]
            }
        }
    
    # ============ MAIN AGENTIC WORKFLOW ============
    
    async def process_message(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """
        Main agentic workflow with LLM-powered decision making and Enhanced RAG
        
        Workflow:
        1. Session management
        2. RAG initialization and enhancement
        3. LLM-based intent analysis with RAG context
        4. Tool selection and invocation
        5. Response generation with RAG
        6. Memory update
        """
        
        # Step 1: Manage session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session_result = await self.tools["session_manager"].func(session_id, "create_or_update")
        
        # Step 1.5: Initialize RAG system if not already done
        if not self.rag_initialized:
            await self.rag_agent.initialize_and_train()
            self.rag_initialized = True
        
        # Step 2: Enhanced mood analysis with RAG context
        conversation_history = self._get_conversation_context(session_id).get("messages", [])
        rag_context = await self.rag_agent.enhanced_retrieval(
            query=message,
            context=conversation_history
        )
        
        mood_analysis = await self.tools["mood_analyzer"].func(message, self._get_conversation_context(session_id))
        
        # Enhance mood analysis with RAG insights
        if rag_context.get("similar_conversations"):
            similar_conversations = rag_context["similar_conversations"]
            if similar_conversations:
                best_match = similar_conversations[0]
                if best_match["similarity_score"] > 0.7:
                    # Use RAG insights to refine mood detection
                    mood_analysis["rag_enhanced"] = True
                    mood_analysis["rag_confidence"] = best_match["similarity_score"]
                    mood_analysis["rag_suggested_category"] = best_match["mood_category"]
        
        # Check for mistake patterns to avoid
        mistake_patterns = rag_context.get("mistake_patterns", [])
        if mistake_patterns:
            for pattern in mistake_patterns:
                if pattern["similarity_score"] > 0.8:
                    # High similarity to a previous mistake - adjust approach
                    mood_analysis["mistake_warning"] = True
                    mood_analysis["previous_error"] = pattern["error_type"]
                    mood_analysis["correction_guidance"] = pattern["correct_response"]
        
        # Step 3: Determine which external tools to invoke
        tools_to_invoke = await self._decide_tool_invocation(message, mood_analysis, session_id)
        
        # Step 4: Execute external tools with RAG enhancement
        tool_results = {}
        for tool_name, params in tools_to_invoke.items():
            if tool_name in self.tools:
                tool_results[tool_name] = await self.tools[tool_name].func(**params)
        
        # Add RAG-retrieved quotes to tool results
        if rag_context.get("semantic_quotes"):
            tool_results["rag_quotes"] = rag_context["semantic_quotes"]
        
        # Step 5: Generate natural response using LLM with RAG enhancement
        response = await self._generate_llm_response(message, mood_analysis, tool_results, session_id, rag_context)
        
        # Step 6: Update conversation memory and train RAG
        self._update_conversation_memory(session_id, message, response, mood_analysis, tool_results)
        
        # Train RAG system with this interaction
        if mood_analysis.get("category") and mood_analysis.get("confidence", 0) > 0.5:
            self.rag_agent.rag_system.add_training_data(
                prompt=message,
                response=response,
                mood_category=mood_analysis["category"],
                confidence=mood_analysis["confidence"]
            )
        
        return {
            "response": response,
            "session_id": session_id,
            "mood_analysis": mood_analysis,
            "tools_invoked": list(tool_results.keys()),
            "tool_results": tool_results,
            "rag_context": rag_context,
            "conversation_context": self._get_conversation_context(session_id)
        }
    
    async def learn_from_feedback(self, message: str, response: str, feedback: str, 
                                session_id: str = None, is_correction: bool = False) -> Dict[str, Any]:
        """Learn from user feedback to improve future responses"""
        try:
            # Get the original mood analysis for this interaction
            session_context = self._get_conversation_context(session_id or "")
            last_interaction = session_context.get("messages", [])[-1] if session_context.get("messages") else {}
            mood_analysis = last_interaction.get("mood_analysis", {})
            
            # Use RAG system to learn from feedback
            await self.rag_agent.learn_from_feedback(
                prompt=message,
                response=response,
                mood_category=mood_analysis.get("category", "general"),
                confidence=mood_analysis.get("confidence", 0.5),
                user_feedback=feedback,
                is_correction=is_correction
            )
            
            # Update session memory with feedback
            if session_id and session_id in self.session_memory:
                if "feedback_history" not in self.session_memory[session_id]:
                    self.session_memory[session_id]["feedback_history"] = []
                
                self.session_memory[session_id]["feedback_history"].append({
                    "message": message,
                    "response": response,
                    "feedback": feedback,
                    "is_correction": is_correction,
                    "timestamp": datetime.now().isoformat()
                })
            
            return {
                "status": "feedback_received",
                "message": "Thank you for the feedback! I'll learn from this to improve future responses.",
                "learning_applied": True
            }
            
        except Exception as e:
            print(f"❌ Feedback learning error: {e}")
            return {
                "status": "error",
                "message": "I had trouble processing your feedback, but I appreciate it!",
                "learning_applied": False
            }
    
    async def _decide_tool_invocation(self, message: str, mood_analysis: Dict[str, Any], session_id: str) -> Dict[str, Dict[str, Any]]:
        """LLM-powered decision making for tool invocation"""
        
        tools_to_invoke = {}
        
        # Always manage conversation
        tools_to_invoke["conversation_manager"] = {
            "message": message,
            "session_id": session_id,
            "history": self._get_conversation_context(session_id).get("messages", [])
        }
        
        detected_mood = mood_analysis.get("category", "general")
        confidence = mood_analysis.get("confidence", 0)
        
        # Always invoke navigation (provide default route if needed)
        tools_to_invoke["quote_navigator"] = {
            "mood": detected_mood,
            "confidence": confidence
        }
        
        # Invoke quotes for specific moods or general quotes for others
        if detected_mood in ["motivational", "romantic", "funny", "inspirational"] and confidence > 0.3:
            tools_to_invoke["quote_fetcher"] = {
                "category": detected_mood,
                "count": 3
            }
        else:
            # For low confidence or general mood, still provide general quotes
            tools_to_invoke["quote_fetcher"] = {
                "category": "general",
                "count": 3
            }
        
        # Provide emotional support for high emotional intensity
        emotional_intensity = mood_analysis.get("emotional_intensity", 0)
        if emotional_intensity > 0.6:
            tools_to_invoke["emotional_support"] = {
                "mood": detected_mood,
                "intensity": emotional_intensity,
                "context": mood_analysis
            }
        
        return tools_to_invoke
    
    # ============ EXTERNAL TOOL IMPLEMENTATIONS ============
    
    async def analyze_mood_with_llm(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced mood analysis with hybrid mode for optimal speed + accuracy"""
        
        # Step 1: Quick pattern check for high-confidence cases
        quick_result = await self._enhanced_pattern_matching(message)
        if quick_result.get("confidence", 0) > 0.85:
            return quick_result
        
        # Step 2: Use appropriate analysis based on mode
        if self.fast_mode:
            return await self._fast_mood_analysis(message)
        elif self.hybrid_mode:
            return await self._hybrid_mood_analysis(message, context)
        else:
            return await self._full_llm_analysis(message, context)
        
        # Enhanced conversation context
        conversation_history = context.get("messages", [])[-3:] if context else []
        history_text = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in conversation_history])
        
        # Use enhanced prompt with better context and examples
        prompt = f"""You are an expert emotional intelligence AI specializing in mood detection for personalized quote recommendations.

CORE MISSION: Accurately classify the user's emotional state to provide the most helpful quote experience.

DETECTION CATEGORIES with enhanced indicators:

1. **motivational** 🎯
   - Primary keywords: goal, achieve, motivation, productivity, challenge, succeed, determination, drive, push, overcome, effort, work, progress, ambition, energy, focus
   - Emotional signals: Feeling stuck, needing drive, wanting accomplishment, lacking energy, facing challenges
   - Context patterns: Work struggles, goal-setting, self-improvement, overcoming obstacles
   - Intensity markers: "really need", "struggling with", "can't seem to", "want to achieve"

2. **romantic** 💕  
   - Primary keywords: love, relationship, heart, partner, dating, valentine, anniversary, crush, feelings, romance, marriage, proposal, boyfriend, girlfriend, husband, wife
   - Emotional signals: Love-related joy/sadness, relationship dynamics, affection needs, longing, celebration
   - Context patterns: Relationship milestones, romantic occasions, dating situations, love expressions
   - Intensity markers: "deeply in love", "miss them so much", "special day", "relationship troubles"

3. **funny** 😄
   - Primary keywords: laugh, humor, joke, cheer, entertainment, lighthearted, comedy, amusing, witty, hilarious, smile, fun, silly, playful
   - Emotional signals: Need for lightness, stress relief through humor, wanting entertainment, feeling down and needing cheering
   - Context patterns: Bad day needing pickup, wanting to share joy, seeking distraction, mood-boosting
   - Intensity markers: "really need to laugh", "cheer me up", "having a terrible day", "need something funny"

4. **inspirational** ✨
   - Primary keywords: meaning, purpose, wisdom, spiritual, hope, faith, guidance, enlightenment, philosophy, life lessons, inspire, deeper, soul, growth
   - Emotional signals: Seeking deeper understanding, life transitions, existential thoughts, need for wisdom
   - Context patterns: Life challenges, seeking guidance, philosophical discussions, personal growth
   - Intensity markers: "searching for meaning", "feeling lost", "need direction", "going through changes"

5. **general** 💬
   - Patterns: Greetings, casual conversation, unclear intent, mixed signals, technical questions

USER PATTERNS:
- Recent moods: {user_profile.get('recent_moods', 'New user')}
- Interaction count: {len(user_profile.get('messages', []))}
- Preferred categories: {user_profile.get('favorite_categories', ['varied'])}

CONVERSATION HISTORY:
{history_text}

CURRENT MESSAGE TO ANALYZE: "{message}"

ENHANCED EXAMPLES:
- "I'm really struggling to stay motivated with my fitness goals" → motivational (confidence: 0.92, intensity: 0.8)
- "My boyfriend surprised me with dinner reservations for our 2-year anniversary!" → romantic (confidence: 0.95, intensity: 0.7)  
- "I desperately need something hilarious to cheer me up after this awful day at work" → funny (confidence: 0.95, intensity: 0.9)
- "I've been questioning what my life's purpose really is lately" → inspirational (confidence: 0.88, intensity: 0.8)

RESPONSE FORMAT (JSON only):
{{
    "category": "motivational|romantic|funny|inspirational|general",
    "confidence": 0.0-1.0,
    "emotional_intensity": 0.0-1.0,
    "reasoning": "detailed step-by-step analysis explaining the classification",
    "primary_indicators": ["strongest", "keywords", "found"],
    "emotional_signals": ["underlying", "emotions", "detected"],
    "user_need": "specific need identified from the message",
    "context_clues": ["relevant", "historical", "patterns"],
    "suggested_quote_themes": ["specific", "themes", "that", "would", "help"],
    "urgency_level": "low|medium|high based on emotional intensity"
}}"""

        try:
            # Call local LLM
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1}  # Low temperature for consistent categorization
            )
            
            # Parse LLM response
            llm_output = response['message']['content']
            
            # Extract JSON from response
            import json
            import re
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                mood_data = json.loads(json_match.group())
                return {
                    "category": mood_data.get("category", "general"),
                    "confidence": float(mood_data.get("confidence", 0.5)),
                    "emotional_intensity": float(mood_data.get("emotional_intensity", 0.3)),
                    "reasoning": mood_data.get("reasoning", "LLM analysis"),
                    "keywords": mood_data.get("keywords", []),
                    "user_need": mood_data.get("user_need", "support"),
                    "analysis_method": "LLM-powered",
                    "timestamp": datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"LLM mood analysis error: {e}")
            # Fallback to basic keyword matching
            return await self._fallback_mood_analysis(message)
        
        return await self._fallback_mood_analysis(message)
    
    async def _fallback_mood_analysis(self, message: str) -> Dict[str, Any]:
        """Fallback mood analysis if LLM fails"""
        message_lower = message.lower()
        
        # Simple keyword matching as fallback
        if any(word in message_lower for word in ["motivation", "goal", "achieve", "productive", "energy"]):
            return {"category": "motivational", "confidence": 0.7, "emotional_intensity": 0.5, "reasoning": "keyword fallback"}
        elif any(word in message_lower for word in ["love", "romantic", "relationship", "heart", "valentine"]):
            return {"category": "romantic", "confidence": 0.7, "emotional_intensity": 0.6, "reasoning": "keyword fallback"}
        elif any(word in message_lower for word in ["funny", "laugh", "humor", "joke", "cheer"]):
            return {"category": "funny", "confidence": 0.7, "emotional_intensity": 0.4, "reasoning": "keyword fallback"}
        elif any(word in message_lower for word in ["inspiration", "meaning", "purpose", "wisdom", "spiritual"]):
            return {"category": "inspirational", "confidence": 0.7, "emotional_intensity": 0.6, "reasoning": "keyword fallback"}
        elif any(word in message_lower for word in ["hello", "hi", "hey", "good morning"]):
            return {"category": "general", "confidence": 0.8, "emotional_intensity": 0.2, "reasoning": "greeting detected"}
        
        return {"category": "general", "confidence": 0.3, "emotional_intensity": 0.3, "reasoning": "default fallback"}
    
    async def _enhanced_pattern_matching(self, message: str) -> Dict[str, Any]:
        """Enhanced pattern matching with higher accuracy"""
        message_lower = message.lower()
        
        # Very high confidence patterns (immediate return)
        patterns = {
            "motivational": {
                "phrases": ["need motivation", "feeling unmotivated", "lack motivation", "no energy", "can't achieve", "struggling with goals", "want to succeed", "need drive", "improve productivity", "working on improving", "get better at"],
                "keywords": ["motivation", "goal", "achieve", "success", "determination", "drive", "energy", "ambition", "productive", "productivity", "improve", "better", "work"],
                "intensity": 0.8
            },
            "romantic": {
                "phrases": ["love my", "in love", "anniversary", "valentine", "romantic dinner", "relationship", "my boyfriend", "my girlfriend", "married life"],
                "keywords": ["love", "romantic", "heart", "relationship", "valentine", "anniversary", "crush", "dating"],
                "intensity": 0.6
            },
            "funny": {
                "phrases": ["make me laugh", "need something funny", "cheer me up", "having a bad day", "feeling down", "need humor", "want to smile"],
                "keywords": ["funny", "laugh", "humor", "joke", "cheer", "smile", "hilarious", "comedy"],
                "intensity": 0.8
            },
            "inspirational": {
                "phrases": ["meaning of life", "feel lost", "need guidance", "life purpose", "searching for answers", "need wisdom", "spiritual journey"],
                "keywords": ["meaning", "purpose", "wisdom", "spiritual", "guidance", "inspiration", "hope", "faith"],
                "intensity": 0.7
            }
        }
        
        for category, data in patterns.items():
            # Check for exact phrases (high confidence)
            phrase_match = any(phrase in message_lower for phrase in data["phrases"])
            if phrase_match:
                return {
                    "category": category,
                    "confidence": 0.92,
                    "emotional_intensity": data["intensity"],
                    "reasoning": f"High-confidence phrase match for {category}",
                    "keywords": [word for word in data["keywords"] if word in message_lower],
                    "user_need": f"{category} support",
                    "analysis_method": "enhanced-pattern-matching",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check for keyword clusters (medium-high confidence)
            keyword_matches = sum(1 for word in data["keywords"] if word in message_lower)
            if keyword_matches >= 2:
                return {
                    "category": category,
                    "confidence": 0.87,
                    "emotional_intensity": data["intensity"] - 0.1,
                    "reasoning": f"Multiple keyword match for {category}",
                    "keywords": [word for word in data["keywords"] if word in message_lower],
                    "user_need": f"{category} support",
                    "analysis_method": "enhanced-pattern-matching", 
                    "timestamp": datetime.now().isoformat()
                }
        
        # Check for greetings
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            return {
                "category": "general",
                "confidence": 0.95,
                "emotional_intensity": 0.2,
                "reasoning": "greeting detected",
                "keywords": ["greeting"],
                "user_need": "friendly interaction",
                "analysis_method": "enhanced-pattern-matching",
                "timestamp": datetime.now().isoformat()
            }
        
        return {"category": "general", "confidence": 0.3, "emotional_intensity": 0.3}
    
    async def _hybrid_mood_analysis(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Hybrid analysis: Fast LLM with optimized prompts for 5-10 second response"""
        
        # Build minimal context for speed
        conversation_history = context.get("messages", [])[-2:] if context else []
        history_text = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}"[:50] for msg in conversation_history])
        
        # Optimized prompt for speed and accuracy
        prompt = f"""Analyze mood for quote recommendation. Be precise and fast.

Categories: motivational, romantic, funny, inspirational, general

Recent context: {history_text}
Current message: "{message}"

Focus on:
- motivational: goals, achievement, energy, productivity, challenges
- romantic: love, relationships, heart, partner, affection  
- funny: humor, laughter, cheer up, entertainment
- inspirational: meaning, purpose, wisdom, guidance, hope
- general: greetings, unclear intent

Respond with JSON only:
{{
    "category": "motivational|romantic|funny|inspirational|general",
    "confidence": 0.0-1.0,
    "emotional_intensity": 0.0-1.0,
    "reasoning": "brief explanation",
    "user_need": "what they need"
}}"""

        try:
            # Optimized LLM call for hybrid mode
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.2,        # Balanced creativity/consistency
                    "num_predict": 150,        # Limit output length
                    "timeout": 8000,           # 8 second timeout
                    "top_k": 10,              # Limit token choices for speed
                    "top_p": 0.9              # Focus on most likely tokens
                }
            )
            
            # Parse response
            llm_output = response['message']['content']
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                try:
                    mood_data = json.loads(json_match.group())
                    category = mood_data.get("category", "general")
                    
                    # Validate category
                    valid_categories = ["motivational", "romantic", "funny", "inspirational", "general"]
                    if category not in valid_categories:
                        category = "general"
                    
                    return {
                        "category": category,
                        "confidence": float(mood_data.get("confidence", 0.6)),
                        "emotional_intensity": float(mood_data.get("emotional_intensity", 0.4)),
                        "reasoning": mood_data.get("reasoning", "Hybrid LLM analysis"),
                        "keywords": [],
                        "user_need": mood_data.get("user_need", "support"),
                        "analysis_method": "hybrid-llm",
                        "timestamp": datetime.now().isoformat()
                    }
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"JSON parsing error: {e}")
                    return await self._fast_mood_analysis(message)
                
        except Exception as e:
            print(f"Hybrid analysis error: {e}")
            # Fallback to enhanced pattern matching
            return await self._fast_mood_analysis(message)
        
        return await self._fast_mood_analysis(message)
    
    async def _full_llm_analysis(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Full LLM analysis with complete context (original method)"""
        # Build enhanced user profile from session context
        user_profile = self._build_user_profile(context)
    
    async def navigate_to_quotes(self, mood: str, confidence: float) -> Dict[str, Any]:
        """Navigate to appropriate quote section"""
        page_mapping = {
            "motivational": "motivational",
            "romantic": "romantic", 
            "funny": "funny",
            "inspirational": "inspirational",
            "general": "motivational",  # Default to motivational for general
            "sad": "inspirational",      # Map sad to inspirational
            "happy": "funny",           # Map happy to funny
            "love": "romantic",         # Map love to romantic
            "work": "motivational",     # Map work to motivational
            "life": "inspirational"     # Map life to inspirational
        }
        
        # Get the appropriate category, default to motivational
        category = page_mapping.get(mood.lower(), "motivational")
        
        return {
            "recommended_page": f"/quotes/{category}",
            "category": category,
            "confidence": confidence,
            "navigation_reasoning": f"Based on {mood} mood with {confidence:.2f} confidence, redirecting to {category} quotes"
        }
    
    async def fetch_relevant_quotes(self, category: str, count: int = 3) -> Dict[str, Any]:
        """Enhanced quote fetching with contextual ranking"""
        try:
            # Get more quotes than needed for better selection
            quotes = DatabaseManager.get_quotes_by_category(category, count * 2)
            
            # Apply simple relevance ranking (can be enhanced further)
            if quotes:
                # Prefer quotes with certain quality indicators
                quality_keywords = ["heart", "soul", "life", "love", "dream", "hope", "strength", "courage", "wisdom"]
                
                scored_quotes = []
                for quote in quotes:
                    quote_text = quote.get("quote", "").lower()
                    
                    # Quality score based on meaningful words
                    quality_score = sum(1 for keyword in quality_keywords if keyword in quote_text)
                    
                    # Length preference (not too long, not too short)
                    word_count = len(quote_text.split())
                    length_score = max(0, 10 - abs(word_count - 15))  # Prefer around 15 words
                    
                    total_score = quality_score * 3 + length_score
                    
                    scored_quotes.append({
                        "quote": quote,
                        "score": total_score
                    })
                
                # Sort by score and return top quotes
                scored_quotes.sort(key=lambda x: x["score"], reverse=True)
                ranked_quotes = [item["quote"] for item in scored_quotes[:count]]
                
                return {
                    "quotes": ranked_quotes,
                    "category": category,
                    "count": len(ranked_quotes),
                    "source": "database_enhanced"
                }
            
            return {
                "quotes": quotes[:count],
                "category": category,
                "count": len(quotes[:count]),
                "source": "database"
            }
        except Exception as e:
            return {"quotes": [], "error": str(e), "category": category}
    
    async def manage_conversation_flow(self, message: str, session_id: str, history: List[Dict]) -> Dict[str, Any]:
        """Manage conversation flow and engagement"""
        return {
            "is_new_conversation": len(history) == 0,
            "message_count": len(history),
            "engagement_level": min(len(history) / 10, 1.0),
            "conversation_stage": "opening" if len(history) < 3 else "ongoing"
        }
    
    async def manage_user_session(self, session_id: str, action: str) -> Dict[str, Any]:
        """Manage user sessions and memory"""
        if session_id not in self.session_memory:
            self.session_memory[session_id] = {
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "mood_history": [],
                "preferences": {}
            }
            return {"action": "session_created", "session_id": session_id}
        else:
            return {"action": "session_updated", "session_id": session_id}
    
    async def provide_emotional_support(self, mood: str, intensity: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide emotional support based on mood and intensity"""
        
        support_messages = {
            "motivational": "Remember, every expert was once a beginner. You have the strength to achieve your goals! 💪",
            "romantic": "Love is a beautiful journey with ups and downs. Your heart's capacity for love is a gift. 💝",
            "funny": "Laughter truly is the best medicine! Keep that beautiful sense of humor alive. 😄",
            "inspirational": "You're exactly where you need to be in your journey. Trust the process and keep growing. ✨"
        }
        
        return {
            "support_provided": intensity > 0.5,
            "support_message": support_messages.get(mood, "You're doing great! Keep going! 🌟"),
            "intensity_level": intensity,
            "mood_addressed": mood
        }
    
    # ============ LLM RESPONSE GENERATION ============
    
    async def _generate_llm_response(self, message: str, mood_analysis: Dict[str, Any], 
                                   tool_results: Dict[str, Any], session_id: str, rag_context: Dict[str, Any] = None) -> str:
        """Enhanced response generation with hybrid mode and RAG support"""
        
        mood_category = mood_analysis.get("category", "general")
        quotes_data = tool_results.get("quote_fetcher", {})
        navigation_data = tool_results.get("quote_navigator", {})
        rag_quotes = tool_results.get("rag_quotes", [])
        
        # Choose response generation method based on mode
        if self.fast_mode:
            return self._fast_response_generation(mood_category, quotes_data, navigation_data, rag_quotes)
        elif self.hybrid_mode:
            return await self._hybrid_response_generation(message, mood_analysis, tool_results, session_id, rag_context)
        else:
            return await self._full_response_generation(message, mood_analysis, tool_results, session_id, rag_context)
    
    async def _hybrid_response_generation(self, message: str, mood_analysis: Dict[str, Any], 
                                        tool_results: Dict[str, Any], session_id: str, rag_context: Dict[str, Any] = None) -> str:
        """Hybrid response: Fast LLM generation with optimized prompts and RAG enhancement"""
        
        mood_category = mood_analysis.get("category", "general")
        confidence = mood_analysis.get("confidence", 0)
        quotes_data = tool_results.get("quote_fetcher", {})
        navigation_data = tool_results.get("quote_navigator", {})
        rag_quotes = tool_results.get("rag_quotes", [])
        
        # Optimized prompt for hybrid mode
        prompt = f"""You are AuraQuotes AI, a warm companion for mood-based quote recommendations.

User said: "{message}"
Detected mood: {mood_category} (confidence: {confidence:.2f})
User needs: {mood_analysis.get('user_need', 'support')}

Response style for {mood_category}:
- motivational: Energetic, empowering
- romantic: Warm, heart-centered  
- funny: Playful, uplifting
- inspirational: Thoughtful, wise
- general: Friendly, welcoming

Create a warm 2-3 sentence response that:
1. Acknowledges their mood naturally
2. Shows understanding
3. Sets up quote presentation

Keep it conversational and caring:"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.6,        # Balanced creativity
                    "num_predict": 100,        # Short response for speed
                    "timeout": 6000,           # 6 second timeout
                    "top_k": 15,              # Moderate choices
                    "top_p": 0.9
                }
            )
            
            llm_response = response['message']['content']
            
            # Add quote - prefer RAG quotes for better relevance
            selected_quote = None
            if rag_quotes and len(rag_quotes) > 0:
                # Use highest relevance RAG quote
                selected_quote = max(rag_quotes, key=lambda q: q.get("relevance_score", 0))
                llm_response += f'\n\n"❝ {selected_quote["quote"]} ❞\n— {selected_quote["author"]} (RAG Enhanced)'
            elif quotes_data.get("quotes"):
                # Fallback to traditional quotes
                first_quote = quotes_data["quotes"][0]
                selected_quote = first_quote
                llm_response += f'\n\n"❝ {first_quote["quote"]} ❞\n— {first_quote["author"]}'
            
            # Add RAG context insights if available
            if rag_context and rag_context.get("similar_conversations"):
                similar_conv = rag_context["similar_conversations"][0]
                if similar_conv.get("similarity_score", 0) > 0.8:
                    llm_response += f"\n\n💡 This reminds me of similar conversations - you're not alone in feeling this way!"
            
            # Add navigation if available
            if navigation_data.get("recommended_page"):
                llm_response += f"\n\n🔗 Explore more {mood_category} quotes: {navigation_data['recommended_page']}"
            
            return llm_response
            
        except Exception as e:
            print(f"Hybrid response generation error: {e}")
            return self._fast_response_generation(mood_category, quotes_data, navigation_data, rag_quotes)
    
    async def _full_response_generation(self, message: str, mood_analysis: Dict[str, Any], 
                                      tool_results: Dict[str, Any], session_id: str, rag_context: Dict[str, Any] = None) -> str:
        """Full response generation with complete context and RAG enhancement"""
        
        # Get user profile for personalization
        user_profile = self._build_user_profile(self._get_conversation_context(session_id))
        
        # Prepare context for response generation
        mood_category = mood_analysis.get("category", "general")
        confidence = mood_analysis.get("confidence", 0)
        quotes_data = tool_results.get("quote_fetcher", {})
        navigation_data = tool_results.get("quote_navigator", {})
        support_data = tool_results.get("emotional_support", {})
        
        user_context = ""
        if user_profile:
            messages_count = len(user_profile.get('messages', []))
            is_returning = messages_count > 0
            user_context = f"""
USER RELATIONSHIP:
- Interaction history: {messages_count} previous messages
- User status: {'Returning friend' if is_returning else 'New friend'}
- Previous successful moods: {user_profile.get('successful_moods', ['varied'])}
"""

        quotes_context = ""
        if quotes_data.get("quotes"):
            quotes_context = f"""
AVAILABLE QUOTES:
{json.dumps(quotes_data["quotes"][:3], indent=2)}
"""

        # Enhanced response generation prompt
        prompt = f"""You are AuraQuotes AI, a warm and emotionally intelligent companion who specializes in mood-based quote recommendations.

YOUR PERSONALITY CORE:
- 💝 EMPATHETIC: You deeply understand and validate emotions without judgment
- 🧠 WISE: You offer thoughtful insights through carefully chosen quotes  
- 🌟 ENCOURAGING: You motivate and uplift while acknowledging real feelings
- 🗣️ AUTHENTIC: You speak naturally like a caring friend, not a corporate bot
- 🎯 ADAPTIVE: You match the user's emotional energy and communication style

{user_context}

CURRENT INTERACTION:
- User said: "{message}"
- Detected mood: {mood_category} (confidence: {confidence:.2f})
- Emotional intensity: {mood_analysis.get('emotional_intensity', 0):.2f}
- User's specific need: {mood_analysis.get('user_need', 'support and connection')}
- Suggested themes: {mood_analysis.get('suggested_quote_themes', [])}

{quotes_context}

RESPONSE CRAFTING GUIDELINES:

1. **EMOTIONAL CONNECTION** (Opening):
   - Acknowledge their feeling with genuine warmth
   - Use phrases like "I can sense...", "It sounds like...", "I understand that..."
   - Mirror their emotional energy appropriately

2. **MOOD-SPECIFIC TONE ADAPTATION**:
   - motivational → Energetic, empowering: "You've got this!", "That inner strength is there!"
   - romantic → Gentle, heart-centered: "Love is beautiful", "Your heart knows..."  
   - funny → Playful, uplifting: "Let's get those good vibes flowing!", "Time for some smiles!"
   - inspirational → Thoughtful, wise: "These moments of seeking...", "Your journey is meaningful..."

3. **QUOTE INTEGRATION** (Natural flow):
   - DON'T announce: "Here's a quote for you..."
   - DO integrate: "This reminds me of something beautiful..." or "There's a wonderful thought that..."
   - Present the quote as part of the conversation, not as a formal presentation

4. **SUPPORTIVE ENGAGEMENT** (Closing):
   - Offer specific encouragement related to their situation
   - Invite continued connection: "How does this resonate with you?" or "Would you like to explore more?"
   - Include relevant emoji (1-2 max) that match the mood

QUALITY STANDARDS:
- Response length: 3-5 sentences total
- Natural conversation flow from acknowledgment → quote → encouragement
- Personal touch that references their specific situation
- Warm, human-like tone that avoids AI-speak

Generate a response that feels like talking to an emotionally intelligent friend who has access to the perfect quotes for every moment:"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7}  # Higher temperature for creative responses
            )
            
            llm_response = response['message']['content']
            
            # Add quote if available
            if quotes_data.get("quotes"):
                first_quote = quotes_data["quotes"][0]
                quote_text = f'\n\n"❝ {first_quote["quote"]} ❞\n— {first_quote["author"]}'
                llm_response += quote_text
            
            # Add navigation if available
            if navigation_data.get("recommended_page"):
                nav_text = f"\n\n🔗 Explore more {mood_category} quotes: {navigation_data['recommended_page']}"
                llm_response += nav_text
            
            return llm_response
            
        except Exception as e:
            print(f"LLM response generation error: {e}")
            return self._fallback_response(mood_category, quotes_data)
    
    def _fast_response_generation(self, mood_category: str, quotes_data: Dict[str, Any], 
                                navigation_data: Dict[str, Any], rag_quotes: List[Dict[str, Any]] = None) -> str:
        """Fast response generation using templates with RAG enhancement"""
        
        # Fast template-based responses
        templates = {
            "motivational": [
                "I can sense you need some motivation! Let me find you something powerful! 💪",
                "Time to ignite that inner fire! Here's something to energize your spirit! ⚡",
                "You've got this! Let me share something to boost your determination! 🚀"
            ],
            "romantic": [
                "I feel the love in your heart! Let me find something beautiful for you! 💕",
                "Romance is in the air! Here's something to warm your heart! 💝",
                "Your heart is speaking - let me share something special! 🌹"
            ],
            "funny": [
                "I can tell you need a good laugh! Let me brighten your day! 😄",
                "Time to turn that frown upside down! Here's something fun! 🎉",
                "Laughter medicine coming right up! This should make you smile! 😊"
            ],
            "inspirational": [
                "I sense you're seeking deeper meaning! Here's something profound! ✨",
                "Your soul is searching for wisdom! Let me share something beautiful! 🌟",
                "Life's bigger questions are calling! Here's some inspiration! 🌅"
            ],
            "general": [
                "Hello there! I'm here to help you find the perfect quote! 👋",
                "Welcome! Let me find something meaningful for you! 🌈",
                "Great to see you! What mood shall we explore today? 🤗"
            ]
        }
        
        # Select response template
        mood_templates = templates.get(mood_category, templates["general"])
        response = random.choice(mood_templates)
        
        # Add quote - prefer RAG quotes for better relevance
        if rag_quotes and len(rag_quotes) > 0:
            # Use highest relevance RAG quote
            selected_quote = max(rag_quotes, key=lambda q: q.get("relevance_score", 0))
            response += f'\n\n"❝ {selected_quote["quote"]} ❞\n— {selected_quote["author"]} (RAG Enhanced)'
        elif quotes_data.get("quotes"):
            # Fallback to traditional quotes
            first_quote = quotes_data["quotes"][0]
            response += f'\n\n"❝ {first_quote["quote"]} ❞\n— {first_quote["author"]}'
        
        # Add navigation if available
        if navigation_data.get("recommended_page"):
            response += f"\n\n🔗 Explore more {mood_category} quotes: {navigation_data['recommended_page']}"
        
        return response
    
    def _fallback_response(self, mood_category: str, quotes_data: Dict[str, Any]) -> str:
        """Fallback response if LLM fails"""
        templates = self.conversation_templates.get("mood_acknowledgments", {})
        response = templates.get(mood_category, ["I'm here to help you find great quotes!"])[0]
        
        if quotes_data.get("quotes"):
            first_quote = quotes_data["quotes"][0]
            response += f'\n\n"❝ {first_quote["quote"]} ❞\n— {first_quote["author"]}'
        
        return response
    
    # ============ HELPER METHODS ============
    
    def _get_conversation_context(self, session_id: str) -> Dict[str, Any]:
        """Get conversation context for session"""
        return self.session_memory.get(session_id, {})
    
    def _build_user_profile(self, session_memory: Dict) -> Dict[str, Any]:
        """Build enhanced user profile from session data"""
        
        if not session_memory:
            return {"messages": [], "recent_moods": [], "favorite_categories": []}
        
        messages = session_memory.get("messages", [])
        mood_history = session_memory.get("mood_history", [])
        
        # Analyze patterns
        recent_moods = [mood.get("category") for mood in mood_history[-5:]]
        mood_counts = {}
        for mood in recent_moods:
            if mood:
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        favorite_categories = [mood for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True)[:2]]
        
        # Determine successful interactions (simplified)
        successful_moods = []
        for message in messages[-3:]:
            if message.get("mood_analysis", {}).get("confidence", 0) > 0.7:
                successful_moods.append(message["mood_analysis"]["category"])
        
        return {
            "messages": messages,
            "recent_moods": recent_moods,
            "favorite_categories": favorite_categories or ["varied"],
            "successful_moods": list(set(successful_moods)),
            "interaction_count": len(messages),
            "avg_confidence": sum(mood.get("confidence", 0) for mood in mood_history) / max(len(mood_history), 1),
            "last_interaction": messages[-1]["timestamp"] if messages else None
        }
    
    def _update_conversation_memory(self, session_id: str, message: str, response: str, 
                                  mood_analysis: Dict[str, Any], tool_results: Dict[str, Any]):
        """Update conversation memory"""
        if session_id not in self.session_memory:
            return
        
        self.session_memory[session_id]["messages"].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "agent_response": response,
            "mood_analysis": mood_analysis,
            "tools_used": list(tool_results.keys())
        })
        
        self.session_memory[session_id]["mood_history"].append(mood_analysis)
        
        # Keep last 10 messages
        if len(self.session_memory[session_id]["messages"]) > 10:
            self.session_memory[session_id]["messages"] = self.session_memory[session_id]["messages"][-10:]

# ============ COMPATIBILITY WRAPPER ============

class AIAgent(AgenticAIAgent):
    """Compatibility wrapper for existing code"""
    
    async def process_message(self, message: str, chat_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Wrapper for existing interface"""
        session_id = None
        if chat_history:
            session_id = chat_history[-1].get("session_id") if chat_history else None
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        result = await super().process_message(message, session_id)
        
        return {
            "response": result["response"],
            "tool_calls": {
                "intent_detection": result["mood_analysis"],
                "navigation": result["tool_results"].get("quote_navigator", {}),
                "quotes_preview": result["tool_results"].get("quote_fetcher", {}).get("quotes", [])
            }
        }
