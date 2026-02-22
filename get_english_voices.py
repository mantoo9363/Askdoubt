import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HEYGENS_API_KEY")
BASE_URL = "https://api.heygen.com/v2"

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_indian_english_voices():
    url = f"{BASE_URL}/voices"
    print("Searching for English (India) voices...")
    
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json().get("data", {}).get("voices", [])
        
        print(f"\n{'Voice ID':<35} | {'Name':<15} | {'Gender'}")
        print("-" * 65)
        
        found = False
        for voice in data:
            # सिर्फ English (India) को फिल्टर करें
            if "English (India)" in voice.get("language", ""):
                found = True
                print(f"{voice['voice_id']:<35} | {voice['name']:<15} | {voice['gender']}")
        
        if not found:
            print("No English (India) voices found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_indian_english_voices()