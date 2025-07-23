#!/usr/bin/env python3
"""
Simple deployment script for KidApp
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting KidApp on port {port}")
    print(f"📱 Frontend: http://localhost:{port}")
    print(f"🔗 API Docs: http://localhost:{port}/docs")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "src.kidapp.api:app",
        host="0.0.0.0",
        port=port,
        reload=True
    ) 