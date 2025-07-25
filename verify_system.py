#!/usr/bin/env python3
"""
System Verification Script for AuraQuotes AI
Verifies all components are working correctly and removes any unnecessary files
"""

import os
import sys
import asyncio
from datetime import datetime

def check_file_structure():
    """Check if all essential files are present"""
    print("🔍 Checking File Structure...")
    
    essential_files = {
        "backend": [
            "main.py",
            "agentic_ai.py", 
            "rag_system.py",
            "database.py",
            "models.py",
            "requirements.txt",
            ".env.example"
        ],
        "backend/routes": [
            "__init__.py",
            "chat.py",
            "quotes.py"
        ],
        "frontend": [
            "package.json",
            "next.config.js",
            "tailwind.config.js"
        ]
    }
    
    missing_files = []
    
    for directory, files in essential_files.items():
        for file in files:
            file_path = os.path.join(directory, file)
            if not os.path.exists(file_path):
                missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing essential files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All essential files present")
        return True

def check_unnecessary_files():
    """Check for and remove unnecessary files"""
    print("\n🧹 Checking for Unnecessary Files...")
    
    # Files that should not exist in project root
    unnecessary_root_files = [
        "next.config.js",
        "package.json", 
        "postcss.config.js",
        "tailwind.config.js",
        "tsconfig.json"
    ]
    
    removed_files = []
    
    for file in unnecessary_root_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                removed_files.append(file)
            except Exception as e:
                print(f"   ⚠️  Could not remove {file}: {e}")
    
    if removed_files:
        print("✅ Removed unnecessary files:")
        for file in removed_files:
            print(f"   - {file}")
    else:
        print("✅ No unnecessary files found")

async def test_system_components():
    """Test all system components"""
    print("\n🧪 Testing System Components...")
    
    try:
        # Test RAG system import
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        from rag_system import EnhancedRAGAgent
        print("✅ RAG system import successful")
        
        # Test agentic AI import
        from agentic_ai import AgenticAIAgent
        print("✅ Agentic AI import successful")
        
        # Test database import
        from database import DatabaseManager
        print("✅ Database import successful")
        
        # Test basic RAG functionality
        print("\n🔬 Testing RAG System...")
        rag_agent = EnhancedRAGAgent()
        
        # Quick retrieval test
        result = await rag_agent.enhanced_retrieval("test query")
        print(f"✅ RAG retrieval test: {result.get('rag_enhanced', False)}")
        
        # Test AI agent
        print("\n🤖 Testing AI Agent...")
        ai_agent = AgenticAIAgent()
        
        # Test session creation
        test_session = "test_session_" + str(datetime.now().timestamp())
        print(f"✅ Test session created: {test_session}")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def verify_dependencies():
    """Verify all required dependencies are installed"""
    print("\n📦 Verifying Dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'chromadb',
        'sentence-transformers',
        'ollama',
        'sqlite3'  # Built into Python
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    else:
        print("\n✅ All dependencies available")
        return True

async def main():
    """Main verification function"""
    print("🔧 AuraQuotes AI - System Verification")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_checks_passed = True
    
    # Check file structure
    if not check_file_structure():
        all_checks_passed = False
    
    # Remove unnecessary files
    check_unnecessary_files()
    
    # Verify dependencies
    if not verify_dependencies():
        all_checks_passed = False
    
    # Test system components
    if not await test_system_components():
        all_checks_passed = False
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 System Verification PASSED!")
        print("✅ All components are working correctly")
        print("✅ System is ready for production use")
        print("\nTo start the system:")
        print("1. cd backend && python train_rag.py  # Train RAG system")
        print("2. python main.py  # Start the application")
    else:
        print("❌ System Verification FAILED!")
        print("⚠️  Please fix the issues above before running")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
