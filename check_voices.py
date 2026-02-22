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

def get_indian_voices():
    url = f"{BASE_URL}/voices"
    print("Connecting to HeyGen...") # Debug Message
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        data = response.json().get("data", {}).get("voices", [])
        
        print(f"{'Voice ID':<35} | {'Name':<15} | {'Language':<20} | {'Gender'}")
        print("-" * 90)
        
        found = False
        for voice in data:
            # Check for Indian languages or accents
            language = voice.get("language", "")
            name = voice.get("name", "")
            
            # Keywords to search for Indian context
            keywords = ["India", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"]
            
            if any(k.lower() in language.lower() for k in keywords):
                found = True
                print(f"{voice['voice_id']:<35} | {name:<15} | {language:<20} | {voice.get('gender')}")
        
        if not found:
            print("No specific Indian voices found using standard filters.")
            print("Trying to print first 5 voices to check data structure:")
            for i, voice in enumerate(data[:5]):
                 print(voice)

    except Exception as e:
        print(f"Error fetching voices: {e}")

# ==========================================
# 👇 MAIN UPDATE: यहाँ से कोड चलना शुरू होगा
# ==========================================
if __name__ == "__main__":
    get_indian_voices()