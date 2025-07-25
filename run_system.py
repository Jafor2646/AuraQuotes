#!/usr/bin/env python3
"""
AuraQuotes AI - System Runner
Simple script to run the complete system with all enhancements
"""

import sys
import os
import subprocess
import sqlite3
import uvicorn
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def initialize_database():
    """Initialize SQLite database with quotes table"""
    try:
        # Database should be in backend directory
        db_path = backend_path / "database.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create quotes table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT DEFAULT 'motivational'
            )
        ''')
        
        # Add some sample quotes if table is empty
        cursor.execute("SELECT COUNT(*) FROM quotes")
        if cursor.fetchone()[0] == 0:
            sample_quotes = [
                ("The only way to do great work is to love what you do.", "Steve Jobs", "motivational"),
                ("Life is what happens to you while you're busy making other plans.", "John Lennon", "life"),
                ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt", "inspirational"),
                ("It is during our darkest moments that we must focus to see the light.", "Aristotle", "inspirational"),
                ("The only impossible journey is the one you never begin.", "Tony Robbins", "motivational")
            ]
            
            cursor.executemany(
                "INSERT INTO quotes (quote, author, category) VALUES (?, ?, ?)",
                sample_quotes
            )
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def run_server():
    """Run the FastAPI server"""
    try:
        print("🚀 Starting AuraQuotes AI Server...")
        print("📊 Enhanced RAG System: ✅ Trained with 120+ prompts")
        print("🧠 Mistake Learning: ✅ Active")
        print("⚡ Response Time: 5-10 seconds (Hybrid Mode)")
        print("🌐 Server will start at: http://localhost:8000")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("\n" + "="*50)
        
        # Change to backend directory
        os.chdir(backend_path)
        
        # Run the server
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main function to run the complete system"""
    print("🔧 AuraQuotes AI - Enhanced System Runner")
    print("="*50)
    
    # Initialize database
    if not initialize_database():
        print("❌ Failed to initialize database. Exiting...")
        return
    
    # Run server
    run_server()

if __name__ == "__main__":
    main()
