import csv
import requests
import time
import sys
import json
from typing import Dict, Any

API_URL = "http://localhost:8000/generate"
REQUEST_TIMEOUT = 60  # 1 minute timeout per request
MAX_RETRIES = 3

def test_api_connection() -> bool:
    """Test if the API is responding"""
    try:
        response = requests.get(f"{API_URL.replace('/generate', '')}/docs", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API connection test failed: {e}")
        return False

def generate_answer(topic: str, age: int = 7) -> str:
    """Generate an answer with retry logic and better error handling"""
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 Generating answer for: '{topic}' (attempt {attempt + 1}/{MAX_RETRIES})")
            
            data = {
                "topic": topic,
                "age": str(age),
                "interests": "science,nature"
            }
            
            response = requests.post(
                API_URL, 
                data=data, 
                timeout=REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the text answer from the response
            if isinstance(result, dict):
                # Try different possible response structures
                answer = (
                    result.get("outputs", {}).get("text", "") or
                    result.get("text", "") or
                    result.get("answer", "") or
                    str(result)
                )
            else:
                answer = str(result)
            
            if answer and answer.strip() and not answer.startswith("[ERROR]"):
                print(f"✅ Successfully generated answer for: '{topic}'")
                return answer.strip()
            else:
                print(f"⚠️ Empty or invalid response for: '{topic}'")
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout on attempt {attempt + 1} for: '{topic}'")
        except requests.exceptions.RequestException as e:
            print(f"🌐 Request error on attempt {attempt + 1} for: '{topic}': {e}")
        except json.JSONDecodeError as e:
            print(f"📄 JSON decode error on attempt {attempt + 1} for: '{topic}': {e}")
        except Exception as e:
            print(f"❌ Unexpected error on attempt {attempt + 1} for: '{topic}': {e}")
        
        if attempt < MAX_RETRIES - 1:
            wait_time = (attempt + 1) * 2  # Exponential backoff
            print(f"⏳ Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
    
    return f"[ERROR] Failed to generate answer after {MAX_RETRIES} attempts"

def main():
    print("🚀 Starting answer generation...")
    
    # Test API connection first
    if not test_api_connection():
        print("❌ Cannot connect to API. Exiting.")
        sys.exit(1)
    
    success_count = 0
    error_count = 0
    
    try:
        with open("test_questions.csv", newline="", encoding="utf-8") as infile, \
             open("wonderbot_outputs.csv", "w", newline="", encoding="utf-8") as outfile:
            
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=["question", "answer"])
            writer.writeheader()
            
            questions = list(reader)
            total_questions = len(questions)
            print(f"📝 Processing {total_questions} questions...")
            
            for i, row in enumerate(questions, 1):
                topic = row["question"]
                print(f"\n📋 Question {i}/{total_questions}: {topic}")
                
                answer = generate_answer(topic)
                writer.writerow({"question": topic, "answer": answer})
                
                if answer.startswith("[ERROR]"):
                    error_count += 1
                else:
                    success_count += 1
                
                # Add delay between requests to avoid rate limiting
                if i < total_questions:
                    time.sleep(2)
                    
    except FileNotFoundError:
        print("❌ test_questions.csv not found!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during processing: {e}")
        sys.exit(1)
    
    print(f"\n📊 Generation Summary:")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📄 Total: {success_count + error_count}")
    
    if error_count > 0:
        print(f"⚠️ Warning: {error_count} questions failed to generate answers")
        if error_count > total_questions * 0.5:  # More than 50% failed
            print("❌ Too many failures. Exiting with error.")
            sys.exit(1)
    
    print("✅ Answer generation completed successfully!")

if __name__ == "__main__":
    main() 