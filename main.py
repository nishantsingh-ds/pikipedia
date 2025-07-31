#!/usr/bin/env python3
"""
WonderBot - AI-powered educational web app for kids
Entry point for deployment
"""

import uvicorn
import os
from src.kidapp.api import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 