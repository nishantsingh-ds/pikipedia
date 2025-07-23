#!/usr/bin/env python3
"""
Setup script to configure environment variables for KidApp
"""

import os
import sys

def setup_environment():
    """Set up environment variables for the application"""
    
    print("🔧 KidApp Environment Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ Found existing {env_file} file")
    else:
        print(f"📝 Creating {env_file} file...")
        
        # Get OpenAI API key from user
        print("\n🔑 OpenAI API Key Setup")
        print("You need an OpenAI API key to use GPT-4 Vision for image analysis.")
        print("Get your API key from: https://platform.openai.com/api-keys")
        
        openai_key = input("\nEnter your OpenAI API key: ").strip()
        
        if not openai_key:
            print("❌ No API key provided. Please set OPENAI_API_KEY manually.")
            return False
        
        # Create .env file
        try:
            with open(env_file, "w") as f:
                f.write(f"OPENAI_API_KEY={openai_key}\n")
                f.write("# Hugging Face API Key (optional, for backward compatibility)\n")
                f.write("HF_API_TOKEN=your_huggingface_token_here\n")
            
            print(f"✅ Created {env_file} file with OpenAI API key")
            
        except Exception as e:
            print(f"❌ Error creating {env_file}: {e}")
            return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        print("   Or set environment variables manually:")
        print("   - OPENAI_API_KEY=your_key_here")
    
    # Verify OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API key is configured")
        return True
    else:
        print("❌ OpenAI API key not found or not set")
        print("Please set OPENAI_API_KEY in your environment or .env file")
        return False

if __name__ == "__main__":
    success = setup_environment()
    if success:
        print("\n🎉 Setup complete! You can now run the application.")
        print("Start the server with: python -m uvicorn src.kidapp.api:app --reload --host 127.0.0.1 --port 8000")
    else:
        print("\n❌ Setup incomplete. Please configure your API keys.")
        sys.exit(1) 