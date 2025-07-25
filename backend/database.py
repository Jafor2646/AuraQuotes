# Database configuration and utilities
import sqlite3
import os
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with required tables and sample data"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tool_calls TEXT,
            FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
        )
    """)
    
    # Create quotes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            quote TEXT,
            author TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert sample quotes
    sample_quotes = [
        # Motivational Quotes (25 quotes)
        ("motivational", "The only way to do great work is to love what you do.", "Steve Jobs"),
        ("motivational", "Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("motivational", "Your limitation—it's only your imagination.", "Unknown"),
        ("motivational", "Great things never come from comfort zones.", "Unknown"),
        ("motivational", "Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("motivational", "The way to get started is to quit talking and begin doing.", "Walt Disney"),
        ("motivational", "Don't be afraid to give up the good to go for the great.", "John D. Rockefeller"),
        ("motivational", "The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("motivational", "It is during our darkest moments that we must focus to see the light.", "Aristotle"),
        ("motivational", "Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("motivational", "The only impossible journey is the one you never begin.", "Tony Robbins"),
        ("motivational", "In the middle of difficulty lies opportunity.", "Albert Einstein"),
        ("motivational", "Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
        ("motivational", "The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
        ("motivational", "Dream bigger. Do bigger.", "Unknown"),
        ("motivational", "Don't stop when you're tired. Stop when you're done.", "Unknown"),
        ("motivational", "Wake up with determination. Go to bed with satisfaction.", "Unknown"),
        ("motivational", "Do something today that your future self will thank you for.", "Sean Patrick Flanery"),
        ("motivational", "Little things make big days.", "Unknown"),
        ("motivational", "It's going to be hard, but hard does not mean impossible.", "Unknown"),
        ("motivational", "Don't wait for opportunity. Create it.", "Unknown"),
        ("motivational", "Sometimes we're tested not to show our weaknesses, but to discover our strengths.", "Unknown"),
        ("motivational", "The key to success is to focus on goals, not obstacles.", "Unknown"),
        ("motivational", "Dream it. Believe it. Build it.", "Unknown"),
        ("motivational", "Difficult roads often lead to beautiful destinations.", "Unknown"),
        
        # Romantic Quotes & Poems (30 quotes/poems)
        ("romantic", "Love is not about how many days, weeks or months you've been together, it's all about how much you love each other every day.", "Unknown"),
        ("romantic", "I have waited for this opportunity for more than half a century, to repeat to you once again my vow of eternal fidelity and everlasting love.", "Gabriel García Márquez"),
        ("romantic", "You know you're in love when you can't fall asleep because reality is finally better than your dreams.", "Dr. Seuss"),
        ("romantic", "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage.", "Lao Tzu"),
        ("romantic", "The best love is the kind that awakens the soul and makes us reach for more.", "Nicholas Sparks"),
        ("romantic", "I love you not only for what you are, but for what I am when I am with you.", "Elizabeth Barrett Browning"),
        ("romantic", "You are my today and all of my tomorrows.", "Leo Christopher"),
        ("romantic", "In all the world, there is no heart for me like yours. In all the world, there is no love for you like mine.", "Maya Angelou"),
        ("romantic", "I love you more than I have ever found a way to say to you.", "Ben Folds"),
        ("romantic", "Every love story is beautiful, but ours is my favorite.", "Unknown"),
        ("romantic", "You are my sun, my moon, and all my stars.", "E.E. Cummings"),
        ("romantic", "Whatever our souls are made of, his and mine are the same.", "Emily Brontë"),
        ("romantic", "I love you begins by I, but it ends up by you.", "Charles de Leusse"),
        ("romantic", "How do I love thee? Let me count the ways. I love thee to the depth and breadth and height my soul can reach.", "Elizabeth Barrett Browning"),
        ("romantic", "Love is friendship that has caught fire. It is quiet understanding, mutual confidence, sharing and forgiving.", "Ann Landers"),
        ("romantic", "Two souls with but a single thought, two hearts that beat as one.", "John Keats"),
        ("romantic", "The water shines only by the sun. And it is you who are my sun.", "Charles de Leusse"),
        ("romantic", "I have found the one whom my soul loves.", "Song of Solomon 3:4"),
        ("romantic", "You are the finest, loveliest, tenderest, and most beautiful person I have ever known—and even that is an understatement.", "F. Scott Fitzgerald"),
        ("romantic", "Grow old with me! The best is yet to be.", "Robert Browning"),
        ("romantic", "If I had a flower for every time I thought of you... I could walk through my garden forever.", "Alfred Tennyson"),
        ("romantic", "I would rather share one lifetime with you than face all the ages of this world alone.", "J.R.R. Tolkien"),
        ("romantic", "Your love is all I need to feel complete.", "Unknown"),
        ("romantic", "When I look into your eyes, I see my future.", "Unknown"),
        ("romantic", "You make my heart skip a beat and my soul dance with joy.", "Unknown"),
        ("romantic", "Love is when you meet someone who tells you something new about yourself.", "André Breton"),
        ("romantic", "I choose you. And I'll choose you over and over and over. Without pause, without a doubt, in a heartbeat. I'll keep choosing you.", "Unknown"),
        ("romantic", "You have bewitched me, body and soul, and I love, I love, I love you.", "Jane Austen"),
        ("romantic", "Meeting you was like listening to a song for the first time and knowing it would be my favorite.", "Unknown"),
        ("romantic", "I fell in love the way you fall asleep: slowly, and then all at once.", "John Green"),
        
        # Funny Quotes (20 quotes)
        ("funny", "I'm not lazy, I'm just on energy saving mode.", "Unknown"),
        ("funny", "I told my wife she was drawing her eyebrows too high. She looked surprised.", "Unknown"),
        ("funny", "Why don't scientists trust atoms? Because they make up everything!", "Unknown"),
        ("funny", "I haven't spoken to my wife in years. I didn't want to interrupt her.", "Rodney Dangerfield"),
        ("funny", "The trouble with having an open mind is that people keep coming along and sticking things into it.", "Terry Pratchett"),
        ("funny", "I'm not arguing, I'm just explaining why I'm right.", "Unknown"),
        ("funny", "I'm not great at the advice. Can I interest you in a sarcastic comment?", "Chandler Bing"),
        ("funny", "Common sense is not so common.", "Voltaire"),
        ("funny", "The best time to plant a tree was 20 years ago. The second best time is now. The third best time is definitely not during a tornado.", "Unknown"),
        ("funny", "I used to hate facial hair, but then it grew on me.", "Unknown"),
        ("funny", "Age is something that doesn't matter, unless you are a cheese.", "Luis Buñuel"),
        ("funny", "Behind every successful person is a substantial amount of coffee.", "Unknown"),
        ("funny", "I'm on a seafood diet. I see food and I eat it.", "Unknown"),
        ("funny", "My bed is a magical place where I suddenly remember everything I forgot to do.", "Unknown"),
        ("funny", "I'm not clumsy, it's just the floor hates me, the tables and chairs are bullies, and the walls get in my way.", "Unknown"),
        ("funny", "Life is short. Smile while you still have teeth.", "Unknown"),
        ("funny", "I don't need a hair stylist, my pillow gives me a new hairstyle every morning.", "Unknown"),
        ("funny", "Monday is an awful way to spend 1/7th of your life.", "Unknown"),
        ("funny", "If you think nobody cares if you're alive, try missing a couple of payments.", "Earl Wilson"),
        ("funny", "The early bird might get the worm, but the second mouse gets the cheese.", "Unknown"),
        
        # Inspirational Quotes (25 quotes)
        ("inspirational", "The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("inspirational", "It is during our darkest moments that we must focus to see the light.", "Aristotle"),
        ("inspirational", "Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("inspirational", "The only impossible journey is the one you never begin.", "Tony Robbins"),
        ("inspirational", "In the middle of difficulty lies opportunity.", "Albert Einstein"),
        ("inspirational", "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "Ralph Waldo Emerson"),
        ("inspirational", "The only person you are destined to become is the person you decide to be.", "Ralph Waldo Emerson"),
        ("inspirational", "Life is what happens to you while you're busy making other plans.", "John Lennon"),
        ("inspirational", "The purpose of our lives is to be happy.", "Dalai Lama"),
        ("inspirational", "Life is really simple, but we insist on making it complicated.", "Confucius"),
        ("inspirational", "May you live all the days of your life.", "Jonathan Swift"),
        ("inspirational", "Life itself is the most wonderful fairy tale.", "Hans Christian Andersen"),
        ("inspirational", "Do not go where the path may lead, go instead where there is no path and leave a trail.", "Ralph Waldo Emerson"),
        ("inspirational", "You have been assigned this mountain to show others it can be moved.", "Mel Robbins"),
        ("inspirational", "Everything you need is inside you – you just need to access it.", "Buddha"),
        ("inspirational", "If you want to lift yourself up, lift up someone else.", "Booker T. Washington"),
        ("inspirational", "The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
        ("inspirational", "A year from now you may wish you had started today.", "Karen Lamb"),
        ("inspirational", "You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
        ("inspirational", "The only way to do great work is to love what you do.", "Steve Jobs"),
        ("inspirational", "If you look at what you have in life, you'll always have more.", "Oprah Winfrey"),
        ("inspirational", "Life is 10% what happens to you and 90% how you react to it.", "Charles R. Swindoll"),
        ("inspirational", "It does not matter how slowly you go as long as you do not stop.", "Confucius"),
        ("inspirational", "Everything has beauty, but not everyone sees it.", "Confucius"),
        ("inspirational", "The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ]
    
    cursor.executemany(
        "INSERT OR IGNORE INTO quotes (category, quote, author) VALUES (?, ?, ?)",
        sample_quotes
    )
    
    conn.commit()
    conn.close()

class DatabaseManager:
    """Database operations manager"""
    
    @staticmethod
    def get_or_create_session(session_id: Optional[str] = None) -> str:
        """Get existing session or create a new one"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if session exists
        cursor.execute("SELECT session_id FROM chat_sessions WHERE session_id = ?", (session_id,))
        if not cursor.fetchone():
            # Create new session
            cursor.execute(
                "INSERT INTO chat_sessions (session_id) VALUES (?)",
                (session_id,)
            )
            conn.commit()
        
        conn.close()
        return session_id

    @staticmethod
    def save_message(session_id: str, role: str, content: str, tool_calls: Optional[Dict[str, Any]] = None):
        """Save a message to the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO chat_messages (session_id, role, content, tool_calls) VALUES (?, ?, ?, ?)",
            (session_id, role, content, json.dumps(tool_calls) if tool_calls else None)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_chat_history(session_id: str) -> List[Dict[str, Any]]:
        """Get chat history for a session"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, tool_calls, timestamp FROM chat_messages WHERE session_id = ? ORDER BY timestamp",
            (session_id,)
        )
        
        messages = []
        for row in cursor.fetchall():
            message = {
                "role": row["role"],
                "content": row["content"],
                "timestamp": row["timestamp"]
            }
            if row["tool_calls"]:
                message["tool_calls"] = json.loads(row["tool_calls"])
            messages.append(message)
        
        conn.close()
        return messages

    @staticmethod
    def get_quotes_by_category(category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get quotes by category"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM quotes WHERE category = ? ORDER BY RANDOM() LIMIT ?",
            (category, limit)
        )
        
        quotes = []
        for row in cursor.fetchall():
            quotes.append({
                "id": row["id"],
                "quote": row["quote"],
                "author": row["author"],
                "category": row["category"]
            })
        
        conn.close()
        return quotes

    @staticmethod
    def get_all_quotes(limit: int = 100) -> List[Dict[str, Any]]:
        """Get all quotes in random order"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT ?", (limit,))
        
        quotes = []
        for row in cursor.fetchall():
            quotes.append({
                "id": row["id"],
                "quote": row["quote"],
                "author": row["author"],
                "category": row["category"],
                "created_at": row["created_at"]
            })
        
        conn.close()
        return quotes

    @staticmethod
    def add_quote(category: str, quote: str, author: str) -> Dict[str, Any]:
        """Add a new quote to the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO quotes (category, quote, author) VALUES (?, ?, ?)",
            (category, quote, author)
        )
        quote_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "id": quote_id,
            "category": category,
            "quote": quote,
            "author": author
        }
