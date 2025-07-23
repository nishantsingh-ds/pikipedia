#!/usr/bin/env python3
"""
Local testing script for WonderBot API
This helps validate fixes before pushing to CI
"""

import requests
import time
import sys
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_generate_endpoint():
    """Test the generate endpoint with a simple question"""
    try:
        data = {
            "topic": "Why is the sky blue?",
            "age": "7"
        }
        
        print("🧪 Testing generate endpoint...")
        response = requests.post(
            "http://localhost:8000/generate", 
            data=data, 
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generate endpoint works!")
            print(f"Response keys: {list(result.keys())}")
            if 'outputs' in result and 'text' in result['outputs']:
                answer = result['outputs']['text']
                print(f"Answer preview: {answer[:100]}...")
            return True
        else:
            print(f"❌ Generate endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generate endpoint error: {e}")
        return False

def test_imports():
    """Test that all required modules can be imported"""
    modules_to_test = [
        "fastapi",
        "uvicorn", 
        "crewai",
        "openai",
        "requests",
        "csv",
        "json"
    ]
    
    failed_imports = []
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def main():
    print("🔧 WonderBot Local Test Suite")
    print("=" * 40)
    
    # Test 1: Import validation
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    # Test 2: Health endpoint
    print("\n2. Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    # Test 3: Generate endpoint
    print("\n3. Testing generate endpoint...")
    generate_ok = test_generate_endpoint()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    print(f"✅ Imports: {'PASS' if imports_ok else 'FAIL'}")
    print(f"✅ Health: {'PASS' if health_ok else 'FAIL'}")
    print(f"✅ Generate: {'PASS' if generate_ok else 'FAIL'}")
    
    all_passed = imports_ok and health_ok and generate_ok
    print(f"\n🎯 Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())