# Advanced RAG System with Vector Database for AuraQuotes
import os
import json
import asyncio
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

class VectorRAGSystem:
    """
    Advanced RAG (Retrieval-Augmented Generation) system with vector embeddings
    for intelligent quote and context retrieval
    """
    
    def __init__(self, persist_directory: str = "./rag_database"):
        self.persist_directory = persist_directory
        self.embedding_model_name = "all-MiniLM-L6-v2"  # Free, fast, good quality
        
        # Initialize components
        self.embedding_model = None
        self.chroma_client = None
        self.quote_collection = None
        self.context_collection = None
        self.training_collection = None
        
        # Training data storage
        self.training_prompts = []
        self.training_responses = []
        
        print("🚀 Initializing Advanced RAG System...")
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all RAG components"""
        try:
            # Initialize embedding model
            print("📊 Loading embedding model...")
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            print(f"✅ Loaded {self.embedding_model_name}")
            
            # Initialize ChromaDB
            print("🗄️ Setting up vector database...")
            self.chroma_client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Create collections
            self._create_collections()
            print("✅ RAG System initialized successfully!")
            
        except Exception as e:
            print(f"❌ RAG initialization error: {e}")
            # Fallback to basic mode
            self.embedding_model = None
            
    def _create_collections(self):
        """Create ChromaDB collections for different data types"""
        try:
            # Quote embeddings collection
            self.quote_collection = self.chroma_client.get_or_create_collection(
                name="quote_embeddings",
                metadata={"description": "Semantic embeddings of quotes for retrieval"}
            )
            
            # Context embeddings collection  
            self.context_collection = self.chroma_client.get_or_create_collection(
                name="context_embeddings",
                metadata={"description": "User context and conversation history embeddings"}
            )
            
            # Training data collection
            self.training_collection = self.chroma_client.get_or_create_collection(
                name="training_embeddings", 
                metadata={"description": "Training prompts and responses for learning"}
            )
            
            print("✅ Vector database collections created")
            
        except Exception as e:
            print(f"❌ Collection creation error: {e}")
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for list of texts"""
        if not self.embedding_model:
            return np.random.rand(len(texts), 384)  # Fallback random embeddings
            
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            print(f"❌ Embedding creation error: {e}")
            return np.random.rand(len(texts), 384)
    
    def add_quotes_to_vector_db(self, quotes: List[Dict[str, Any]]):
        """Add quotes to vector database with semantic embeddings"""
        if not quotes or not self.quote_collection:
            return
            
        try:
            # Prepare quote texts for embedding
            quote_texts = []
            quote_ids = []
            quote_metadata = []
            
            for i, quote in enumerate(quotes):
                quote_text = f"{quote.get('quote', '')} - {quote.get('author', 'Unknown')}"
                quote_texts.append(quote_text)
                quote_ids.append(f"quote_{quote.get('id', i)}")
                
                # Clean metadata (ChromaDB doesn't allow None values)
                metadata = {
                    "category": quote.get("category") or "general",
                    "author": quote.get("author") or "Unknown",
                    "original_quote": quote.get("quote") or "",
                    "source": "database"
                }
                quote_metadata.append(metadata)
            
            # Create embeddings
            embeddings = self.create_embeddings(quote_texts)
            
            # Add to ChromaDB
            self.quote_collection.add(
                embeddings=embeddings.tolist(),
                documents=quote_texts,
                metadatas=quote_metadata,
                ids=quote_ids
            )
            
            print(f"✅ Added {len(quotes)} quotes to vector database")
            
        except Exception as e:
            print(f"❌ Error adding quotes to vector DB: {e}")
    
    def semantic_quote_search(self, query: str, category: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search for relevant quotes"""
        if not self.quote_collection or not self.embedding_model:
            return []
            
        try:
            # Create query embedding
            query_embedding = self.create_embeddings([query])[0]
            
            # Build where filter for category
            where_filter = {}
            if category and category != "general":
                where_filter = {"category": category}
            
            # Search in vector database
            results = self.quote_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=limit,
                where=where_filter if where_filter else None
            )
            
            # Format results
            semantic_quotes = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i]
                    distance = results["distances"][0][i] if "distances" in results else 0
                    
                    semantic_quotes.append({
                        "quote": metadata["original_quote"],
                        "author": metadata["author"],
                        "category": metadata["category"],
                        "relevance_score": 1 - distance,  # Convert distance to similarity
                        "source": "semantic_search"
                    })
            
            return semantic_quotes
            
        except Exception as e:
            print(f"❌ Semantic search error: {e}")
            return []
    
    def add_training_data(self, prompt: str, response: str, mood_category: str, confidence: float, feedback: str = None):
        """Add training data to vector database for learning with feedback support"""
        if not self.training_collection:
            return
            
        try:
            # Create training document with feedback
            training_text = f"User: {prompt}\nMood: {mood_category}\nResponse: {response}"
            if feedback:
                training_text += f"\nFeedback: {feedback}"
            
            training_id = f"training_{len(self.training_prompts)}_{datetime.now().timestamp()}"
            
            # Create embedding
            embedding = self.create_embeddings([training_text])[0]
            
            # Clean metadata (ChromaDB doesn't allow None values)
            metadata = {
                "prompt": prompt or "",
                "response": response or "",
                "mood_category": mood_category or "general",
                "confidence": float(confidence) if confidence is not None else 0.0,
                "feedback": feedback or "",
                "timestamp": datetime.now().isoformat(),
                "quality_score": float(self._calculate_quality_score(confidence, feedback))
            }
            
            # Add to collection
            self.training_collection.add(
                embeddings=[embedding.tolist()],
                documents=[training_text],
                metadatas=[metadata],
                ids=[training_id]
            )
            
            # Store locally too
            self.training_prompts.append(prompt)
            self.training_responses.append(response)
            
        except Exception as e:
            print(f"❌ Training data addition error: {e}")
    
    def _calculate_quality_score(self, confidence: float, feedback: str = None) -> float:
        """Calculate quality score based on confidence and feedback"""
        base_score = confidence
        
        if feedback:
            feedback_lower = feedback.lower()
            # Positive feedback indicators
            if any(word in feedback_lower for word in ['good', 'great', 'perfect', 'helpful', 'thanks', 'exactly']):
                base_score += 0.2
            # Negative feedback indicators
            elif any(word in feedback_lower for word in ['wrong', 'bad', 'incorrect', 'not helpful', 'mistake']):
                base_score -= 0.3
            # Neutral/correction feedback
            elif any(word in feedback_lower for word in ['better', 'different', 'more', 'less']):
                base_score -= 0.1
                
        return max(0.0, min(1.0, base_score))  # Clamp between 0 and 1
    
    def add_mistake_correction(self, original_prompt: str, incorrect_response: str, correct_response: str, 
                             error_type: str, user_feedback: str):
        """Add mistake correction data for learning"""
        if not self.training_collection:
            return
            
        try:
            # Create correction document
            correction_text = f"User: {original_prompt}\nIncorrect: {incorrect_response}\nCorrect: {correct_response}\nError: {error_type}\nFeedback: {user_feedback}"
            correction_id = f"correction_{datetime.now().timestamp()}"
            
            # Create embedding
            embedding = self.create_embeddings([correction_text])[0]
            
            # Clean metadata (ChromaDB doesn't allow None values)
            metadata = {
                "prompt": original_prompt or "",
                "incorrect_response": incorrect_response or "",
                "correct_response": correct_response or "",
                "error_type": error_type or "general",
                "user_feedback": user_feedback or "",
                "timestamp": datetime.now().isoformat(),
                "is_correction": True,
                "quality_score": 0.9  # High quality for corrections
            }
            
            # Add to collection with high importance
            self.training_collection.add(
                embeddings=[embedding.tolist()],
                documents=[correction_text],
                metadatas=[metadata],
                ids=[correction_id]
            )
            
            print(f"✅ Added mistake correction for: {error_type}")
            
        except Exception as e:
            print(f"❌ Mistake correction error: {e}")
    
    def find_similar_conversations(self, current_prompt: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Find similar past conversations for context with quality filtering"""
        if not self.training_collection:
            return []
            
        try:
            # Create query embedding
            query_embedding = self.create_embeddings([current_prompt])[0]
            
            # Search for similar conversations, prioritizing high-quality ones
            results = self.training_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=limit * 2,  # Get more to filter by quality
                where={"quality_score": {"$gte": 0.5}}  # Only high-quality interactions
            )
            
            # Format results and sort by quality
            similar_conversations = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i]
                    distance = results["distances"][0][i] if "distances" in results else 0
                    
                    # Skip corrections for general similarity search
                    if metadata.get("is_correction", False):
                        continue
                    
                    similar_conversations.append({
                        "prompt": metadata["prompt"],
                        "response": metadata["response"],
                        "mood_category": metadata["mood_category"],
                        "confidence": metadata["confidence"],
                        "similarity_score": 1 - distance,
                        "quality_score": metadata.get("quality_score", 0.5),
                        "timestamp": metadata["timestamp"]
                    })
            
            # Sort by combined similarity and quality score
            similar_conversations.sort(
                key=lambda x: (x["similarity_score"] * 0.6 + x["quality_score"] * 0.4), 
                reverse=True
            )
            
            return similar_conversations[:limit]
            
        except Exception as e:
            print(f"❌ Similar conversation search error: {e}")
            return []
    
    def find_mistake_patterns(self, current_prompt: str) -> List[Dict[str, Any]]:
        """Find similar mistake patterns to avoid repeating errors"""
        if not self.training_collection:
            return []
            
        try:
            # Create query embedding
            query_embedding = self.create_embeddings([current_prompt])[0]
            
            # Search specifically for corrections
            results = self.training_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=5,
                where={"is_correction": True}
            )
            
            # Format correction results
            mistake_patterns = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i]
                    distance = results["distances"][0][i] if "distances" in results else 0
                    
                    mistake_patterns.append({
                        "original_prompt": metadata["prompt"],
                        "incorrect_response": metadata["incorrect_response"],
                        "correct_response": metadata["correct_response"],
                        "error_type": metadata["error_type"],
                        "user_feedback": metadata["user_feedback"],
                        "similarity_score": 1 - distance,
                        "timestamp": metadata["timestamp"]
                    })
            
            # Sort by similarity
            mistake_patterns.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return mistake_patterns[:3]  # Return top 3 most similar mistakes
            
        except Exception as e:
            print(f"❌ Mistake pattern search error: {e}")
            return []
    
    def get_contextual_embeddings(self, user_message: str, conversation_history: List[str]) -> Dict[str, Any]:
        """Create contextual embeddings from user message and history"""
        try:
            # Combine current message with recent history
            context_window = conversation_history[-3:] if conversation_history else []
            full_context = " ".join(context_window + [user_message])
            
            # Create embedding
            context_embedding = self.create_embeddings([full_context])[0]
            
            return {
                "context_embedding": context_embedding.tolist(),
                "context_text": full_context,
                "message_embedding": self.create_embeddings([user_message])[0].tolist(),
                "history_length": len(context_window)
            }
            
        except Exception as e:
            print(f"❌ Contextual embedding error: {e}")
            return {"context_embedding": [], "context_text": user_message}

class RAGTrainingSystem:
    """Training system for RAG with 100+ diverse prompts"""
    
    def __init__(self, rag_system: VectorRAGSystem):
        self.rag_system = rag_system
        self.training_dataset = self._create_training_dataset()
        
    def _create_training_dataset(self) -> List[Dict[str, Any]]:
        """Create comprehensive training dataset with 100+ prompts"""
        return [
            # Motivational (25 examples)
            {"prompt": "I need motivation for my fitness goals", "category": "motivational", "confidence": 0.9},
            {"prompt": "Feeling unmotivated to study for exams", "category": "motivational", "confidence": 0.85},
            {"prompt": "Can't seem to achieve my career objectives", "category": "motivational", "confidence": 0.8},
            {"prompt": "Struggling with productivity at work", "category": "motivational", "confidence": 0.75},
            {"prompt": "Need energy to pursue my dreams", "category": "motivational", "confidence": 0.9},
            {"prompt": "Lost my drive for personal growth", "category": "motivational", "confidence": 0.8},
            {"prompt": "Want to succeed but feeling stuck", "category": "motivational", "confidence": 0.85},
            {"prompt": "Looking for determination to overcome challenges", "category": "motivational", "confidence": 0.9},
            {"prompt": "Need push to start my business", "category": "motivational", "confidence": 0.8},
            {"prompt": "Feeling lazy about my workout routine", "category": "motivational", "confidence": 0.7},
            {"prompt": "Can't find motivation to learn new skills", "category": "motivational", "confidence": 0.8},
            {"prompt": "Procrastinating on important projects", "category": "motivational", "confidence": 0.75},
            {"prompt": "Need inspiration to achieve excellence", "category": "motivational", "confidence": 0.85},
            {"prompt": "Struggling to maintain discipline", "category": "motivational", "confidence": 0.8},
            {"prompt": "Want to improve my performance", "category": "motivational", "confidence": 0.7},
            {"prompt": "Looking for strength to persevere", "category": "motivational", "confidence": 0.85},
            {"prompt": "Need courage to take risks", "category": "motivational", "confidence": 0.8},
            {"prompt": "Feeling defeated by setbacks", "category": "motivational", "confidence": 0.9},
            {"prompt": "Want to build better habits", "category": "motivational", "confidence": 0.75},
            {"prompt": "Need focus for my goals", "category": "motivational", "confidence": 0.8},
            {"prompt": "Lacking ambition lately", "category": "motivational", "confidence": 0.75},
            {"prompt": "Want to be more productive", "category": "motivational", "confidence": 0.7},
            {"prompt": "Need self-discipline", "category": "motivational", "confidence": 0.8},
            {"prompt": "Struggling with consistency", "category": "motivational", "confidence": 0.75},
            {"prompt": "Want to achieve my potential", "category": "motivational", "confidence": 0.85},
            
            # Romantic (25 examples)
            {"prompt": "My anniversary is coming up", "category": "romantic", "confidence": 0.9},
            {"prompt": "I love my partner so much", "category": "romantic", "confidence": 0.95},
            {"prompt": "Planning a romantic dinner", "category": "romantic", "confidence": 0.85},
            {"prompt": "Valentine's Day is approaching", "category": "romantic", "confidence": 0.9},
            {"prompt": "Missing my boyfriend while he's away", "category": "romantic", "confidence": 0.8},
            {"prompt": "Feeling romantic today", "category": "romantic", "confidence": 0.85},
            {"prompt": "Want to express my love", "category": "romantic", "confidence": 0.8},
            {"prompt": "Planning to propose soon", "category": "romantic", "confidence": 0.9},
            {"prompt": "Celebrating our relationship milestone", "category": "romantic", "confidence": 0.85},
            {"prompt": "Need romantic inspiration", "category": "romantic", "confidence": 0.8},
            {"prompt": "Thinking about my crush", "category": "romantic", "confidence": 0.7},
            {"prompt": "Heart is full of love", "category": "romantic", "confidence": 0.85},
            {"prompt": "Dating someone special", "category": "romantic", "confidence": 0.75},
            {"prompt": "In a new relationship", "category": "romantic", "confidence": 0.8},
            {"prompt": "Long distance relationship struggles", "category": "romantic", "confidence": 0.75},
            {"prompt": "Wedding anniversary celebration", "category": "romantic", "confidence": 0.9},
            {"prompt": "Feeling grateful for my partner", "category": "romantic", "confidence": 0.85},
            {"prompt": "Romance is in the air", "category": "romantic", "confidence": 0.8},
            {"prompt": "Planning romantic surprise", "category": "romantic", "confidence": 0.85},
            {"prompt": "Love letters and poetry", "category": "romantic", "confidence": 0.8},
            {"prompt": "Couple's getaway weekend", "category": "romantic", "confidence": 0.75},
            {"prompt": "Honeymoon planning", "category": "romantic", "confidence": 0.85},
            {"prompt": "Romantic movie night", "category": "romantic", "confidence": 0.7},
            {"prompt": "Growing old together", "category": "romantic", "confidence": 0.8},
            {"prompt": "Soulmate connection", "category": "romantic", "confidence": 0.9},
            
            # Funny (25 examples)
            {"prompt": "Having a terrible day, need something funny", "category": "funny", "confidence": 0.95},
            {"prompt": "Make me laugh please", "category": "funny", "confidence": 0.9},
            {"prompt": "Need humor to cheer me up", "category": "funny", "confidence": 0.85},
            {"prompt": "Want something hilarious", "category": "funny", "confidence": 0.8},
            {"prompt": "Bad day at work, need comedy", "category": "funny", "confidence": 0.9},
            {"prompt": "Feeling down, need a smile", "category": "funny", "confidence": 0.85},
            {"prompt": "Want to laugh until I cry", "category": "funny", "confidence": 0.8},
            {"prompt": "Need entertainment and jokes", "category": "funny", "confidence": 0.75},
            {"prompt": "Monday blues, need humor", "category": "funny", "confidence": 0.8},
            {"prompt": "Stressed out, need comic relief", "category": "funny", "confidence": 0.85},
            {"prompt": "Want witty and amusing content", "category": "funny", "confidence": 0.7},
            {"prompt": "Need lighthearted fun", "category": "funny", "confidence": 0.75},
            {"prompt": "Feeling silly and playful", "category": "funny", "confidence": 0.8},
            {"prompt": "Want to giggle and be happy", "category": "funny", "confidence": 0.75},
            {"prompt": "Need dose of laughter", "category": "funny", "confidence": 0.8},
            {"prompt": "Looking for comedy gold", "category": "funny", "confidence": 0.75},
            {"prompt": "Want something amusing", "category": "funny", "confidence": 0.7},
            {"prompt": "Need to brighten my mood", "category": "funny", "confidence": 0.8},
            {"prompt": "Want funny stories", "category": "funny", "confidence": 0.75},
            {"prompt": "Need cheerful content", "category": "funny", "confidence": 0.7},
            {"prompt": "Want to be entertained", "category": "funny", "confidence": 0.65},
            {"prompt": "Looking for humor therapy", "category": "funny", "confidence": 0.8},
            {"prompt": "Need joke to lift spirits", "category": "funny", "confidence": 0.75},
            {"prompt": "Want playful and fun", "category": "funny", "confidence": 0.7},
            {"prompt": "Need laughter medicine", "category": "funny", "confidence": 0.8},
            
            # Inspirational (25 examples)
            {"prompt": "What's the meaning of life?", "category": "inspirational", "confidence": 0.9},
            {"prompt": "Feeling lost and need guidance", "category": "inspirational", "confidence": 0.85},
            {"prompt": "Searching for my purpose", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Need wisdom for life's journey", "category": "inspirational", "confidence": 0.85},
            {"prompt": "Going through spiritual awakening", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Seeking deeper understanding", "category": "inspirational", "confidence": 0.75},
            {"prompt": "Need hope during dark times", "category": "inspirational", "confidence": 0.9},
            {"prompt": "Looking for enlightenment", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Want philosophical insights", "category": "inspirational", "confidence": 0.75},
            {"prompt": "Questioning my beliefs", "category": "inspirational", "confidence": 0.7},
            {"prompt": "Need spiritual guidance", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Searching for inner peace", "category": "inspirational", "confidence": 0.85},
            {"prompt": "Want to grow as a person", "category": "inspirational", "confidence": 0.75},
            {"prompt": "Need inspiration for change", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Looking for life lessons", "category": "inspirational", "confidence": 0.75},
            {"prompt": "Want meaningful existence", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Seeking truth and wisdom", "category": "inspirational", "confidence": 0.85},
            {"prompt": "Need direction in life", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Want to find my calling", "category": "inspirational", "confidence": 0.75},
            {"prompt": "Going through transformation", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Need faith and hope", "category": "inspirational", "confidence": 0.85},
            {"prompt": "Searching for enlightenment", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Want spiritual growth", "category": "inspirational", "confidence": 0.75},
            {"prompt": "Need deeper meaning", "category": "inspirational", "confidence": 0.8},
            {"prompt": "Looking for divine guidance", "category": "inspirational", "confidence": 0.85},
            
            # General/Mixed (20 examples)
            {"prompt": "Hello there!", "category": "general", "confidence": 0.95},
            {"prompt": "Good morning!", "category": "general", "confidence": 0.9},
            {"prompt": "How are you today?", "category": "general", "confidence": 0.85},
            {"prompt": "Tell me about quotes", "category": "general", "confidence": 0.8},
            {"prompt": "What can you help me with?", "category": "general", "confidence": 0.75},
            {"prompt": "I'm feeling mixed emotions", "category": "general", "confidence": 0.6},
            {"prompt": "Not sure what I need", "category": "general", "confidence": 0.5},
            {"prompt": "Random thought for today", "category": "general", "confidence": 0.6},
            {"prompt": "Tell me something interesting", "category": "general", "confidence": 0.7},
            {"prompt": "I'm bored", "category": "general", "confidence": 0.65},
            {"prompt": "Just saying hi", "category": "general", "confidence": 0.9},
            {"prompt": "Testing the system", "category": "general", "confidence": 0.8},
            {"prompt": "What's new?", "category": "general", "confidence": 0.75},
            {"prompt": "Give me a quote", "category": "general", "confidence": 0.7},
            {"prompt": "Surprise me", "category": "general", "confidence": 0.65},
            {"prompt": "I'm feeling okay", "category": "general", "confidence": 0.6},
            {"prompt": "Not sure how I feel", "category": "general", "confidence": 0.5},
            {"prompt": "Just browsing", "category": "general", "confidence": 0.7},
            {"prompt": "Looking around", "category": "general", "confidence": 0.65},
            {"prompt": "Curious about this app", "category": "general", "confidence": 0.75}
        ]
    
    async def train_rag_system(self):
        """Train RAG system with comprehensive dataset"""
        print("🎓 Starting RAG Training with 100+ prompts...")
        
        for i, training_example in enumerate(self.training_dataset):
            prompt = training_example["prompt"]
            category = training_example["category"]
            confidence = training_example["confidence"]
            
            # Generate training response
            response = self._generate_training_response(prompt, category, confidence)
            
            # Add to RAG system
            self.rag_system.add_training_data(prompt, response, category, confidence)
            
            if (i + 1) % 20 == 0:
                print(f"✅ Trained on {i + 1}/{len(self.training_dataset)} prompts")
        
        print(f"🎉 RAG Training Complete! Trained on {len(self.training_dataset)} prompts")
    
    def _generate_training_response(self, prompt: str, category: str, confidence: float) -> str:
        """Generate appropriate training response for each prompt"""
        response_templates = {
            "motivational": [
                "I can sense you need motivation! Remember, every expert was once a beginner. You have the strength within you to achieve your goals. Keep pushing forward! 💪",
                "You've got this! Sometimes the journey feels tough, but that's where growth happens. Your determination will carry you through any challenge.",
                "I believe in your potential! Every small step you take is progress. Don't underestimate the power of consistent effort and self-belief."
            ],
            "romantic": [
                "Love is such a beautiful thing! Your heart is full of wonderful feelings, and that's something truly special. Cherish these moments of connection. 💕",
                "Romance brings such joy to life! Whether it's celebrating love or nurturing a relationship, your heart knows what's meaningful to you.",
                "What a lovely sentiment! Love in all its forms - romantic, caring, devoted - is one of life's greatest gifts. Your heart is in a beautiful place."
            ],
            "funny": [
                "I can tell you need some laughter! Life's too short not to smile, and sometimes a good laugh is exactly what we need to brighten our day. 😄",
                "Time to turn that frown upside down! Humor has this amazing power to lift our spirits and remind us that joy can be found even in tough moments.",
                "Laughter truly is the best medicine! Let's find something to make you smile and bring some lightness to your day."
            ],
            "inspirational": [
                "What a profound question! Life's journey is about discovering meaning through our experiences, connections, and growth. You're exactly where you need to be. ✨",
                "Seeking wisdom shows a beautiful depth to your soul. These moments of questioning and searching are often when we find our greatest insights.",
                "Your spiritual journey is uniquely yours. Trust the process, embrace the questions, and know that seeking deeper meaning is itself meaningful."
            ],
            "general": [
                "Hello! I'm here to help you find quotes that resonate with your current mood and needs. What's on your mind today?",
                "Great to connect with you! I'd love to help you discover some meaningful quotes. How are you feeling right now?",
                "Welcome! I'm your companion for finding the perfect quotes for any moment. What would you like to explore?"
            ]
        }
        
        templates = response_templates.get(category, response_templates["general"])
        # Use confidence to select template variation
        template_index = min(int(confidence * len(templates)), len(templates) - 1)
        return templates[template_index]

# Integration with existing agentic AI system
class EnhancedRAGAgent:
    """Enhanced agentic AI with full RAG capabilities"""
    
    def __init__(self):
        self.rag_system = VectorRAGSystem()
        self.training_system = RAGTrainingSystem(self.rag_system)
        self.is_trained = False
    
    async def initialize_and_train(self):
        """Initialize RAG system and train with comprehensive dataset"""
        print("🚀 Initializing Enhanced RAG Agent...")
        
        # Train the RAG system
        await self.training_system.train_rag_system()
        
        # Load quotes into vector database
        await self._load_quotes_to_rag()
        
        self.is_trained = True
        print("✅ Enhanced RAG Agent ready!")
    
    async def _load_quotes_to_rag(self):
        """Load existing quotes into RAG vector database"""
        try:
            from database import DatabaseManager
            
            # Get all quotes from database
            all_quotes = []
            categories = ["motivational", "romantic", "funny", "inspirational"]
            
            for category in categories:
                category_quotes = DatabaseManager.get_quotes_by_category(category, 50)
                all_quotes.extend(category_quotes)
            
            # Add to vector database
            self.rag_system.add_quotes_to_vector_db(all_quotes)
            print(f"✅ Loaded {len(all_quotes)} quotes into RAG system")
            
        except Exception as e:
            print(f"❌ Error loading quotes to RAG: {e}")
    
    async def enhanced_retrieval(self, query: str, category: str = None, context: List[str] = None) -> Dict[str, Any]:
        """Perform enhanced contextual retrieval using RAG with mistake avoidance"""
        if not self.is_trained:
            await self.initialize_and_train()
        
        try:
            # Get contextual embeddings
            contextual_data = self.rag_system.get_contextual_embeddings(query, context or [])
            
            # Semantic quote search
            semantic_quotes = self.rag_system.semantic_quote_search(query, category, limit=5)
            
            # Find similar past conversations (high-quality only)
            similar_conversations = self.rag_system.find_similar_conversations(query, limit=3)
            
            # Find mistake patterns to avoid
            mistake_patterns = self.rag_system.find_mistake_patterns(query)
            
            return {
                "semantic_quotes": semantic_quotes,
                "similar_conversations": similar_conversations,
                "mistake_patterns": mistake_patterns,
                "contextual_data": contextual_data,
                "rag_enhanced": True
            }
            
        except Exception as e:
            print(f"❌ Enhanced retrieval error: {e}")
            return {"semantic_quotes": [], "similar_conversations": [], "mistake_patterns": [], "rag_enhanced": False}
    
    async def learn_from_feedback(self, prompt: str, response: str, mood_category: str, 
                                confidence: float, user_feedback: str, is_correction: bool = False):
        """Learn from user feedback to improve future responses"""
        try:
            if is_correction:
                # This is a correction - extract the correct approach
                feedback_lower = user_feedback.lower()
                
                # Determine error type
                if "wrong mood" in feedback_lower or "incorrect category" in feedback_lower:
                    error_type = "mood_detection_error"
                elif "wrong quote" in feedback_lower or "irrelevant quote" in feedback_lower:
                    error_type = "quote_selection_error"
                elif "tone" in feedback_lower or "style" in feedback_lower:
                    error_type = "response_tone_error"
                else:
                    error_type = "general_error"
                
                # Add correction data
                self.rag_system.add_mistake_correction(
                    original_prompt=prompt,
                    incorrect_response=response,
                    correct_response=user_feedback,  # User provides correct approach
                    error_type=error_type,
                    user_feedback=user_feedback
                )
            else:
                # Regular feedback - update training data with quality score
                self.rag_system.add_training_data(
                    prompt=prompt,
                    response=response,
                    mood_category=mood_category,
                    confidence=confidence,
                    feedback=user_feedback
                )
            
            print(f"✅ Learned from feedback: {user_feedback[:50]}...")
            
        except Exception as e:
            print(f"❌ Feedback learning error: {e}")
