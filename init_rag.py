#!/usr/bin/env python3
"""
RAG Database Initialization Script
Run this script to initialize the RAG system with training data on a new deployment
"""

import os
import sys
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from rag_system import EnhancedRAGAgent

async def initialize_rag_system():
    """Initialize RAG system with training data"""
    print("🚀 Initializing RAG System for AuraQuotes...")
    print("=" * 50)
    
    try:
        # Initialize RAG agent
        rag_agent = EnhancedRAGAgent()
        
        # Initialize and train the system
        print("📊 Setting up vector database and training...")
        await rag_agent.initialize_and_train()
        
        print("✅ RAG System initialized successfully!")
        print("📈 Training data: 120+ prompts loaded")
        print("🗄️ Vector database: Created and ready")
        print("🧠 Embedding model: all-MiniLM-L6-v2 loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG initialization failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 AuraQuotes RAG Database Initialization")
    print("This script will set up the RAG system for first-time deployment")
    print("=" * 60)
    
    # Check if already initialized
    rag_db_path = backend_path / "rag_database"
    if rag_db_path.exists() and any(rag_db_path.iterdir()):
        print("⚠️  RAG database already exists!")
        response = input("Do you want to reinitialize? (y/N): ")
        if response.lower() != 'y':
            print("📊 Using existing RAG database")
            return
    
    # Run initialization
    success = asyncio.run(initialize_rag_system())
    
    if success:
        print("\n🎉 Setup Complete!")
        print("Your AuraQuotes AI is now ready with:")
        print("✅ 120+ training prompts")
        print("✅ Vector embeddings for semantic search")
        print("✅ Mistake learning capabilities")
        print("✅ Contextual retrieval system")
        print("\n🚀 Start the server with: python run_system.py")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
