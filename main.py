# AuraQuotes - AI-Powered Quote Platform
# Run this file from the project root to start the application

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main entry point for AuraQuotes application"""
    
    print("🌟 AuraQuotes - AI-Powered Quote Platform")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    print(f"📁 Project root: {project_root}")
    print(f"🔧 Backend directory: {backend_dir}")
    print(f"🎨 Frontend directory: {frontend_dir}")
    print()
    
    # Check if required files exist
    if not (backend_dir / "main.py").exists():
        print("❌ Backend main.py not found!")
        return
    
    if not (backend_dir / "requirements.txt").exists():
        print("❌ Backend requirements.txt not found!")
        return
    
    print("🚀 Starting AuraQuotes Backend Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print()
    print("💡 To start the frontend separately, run: npm run dev (in frontend directory)")
    print("🔗 Frontend will be available at: http://localhost:3000")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
