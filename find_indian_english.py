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

def find_specific_voices():
    url = f"{BASE_URL}/voices"
    print("Searching for specific Indian English voices by Name...")
    
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json().get("data", {}).get("voices", [])
        
        # हम इन नामों को ढूंढेंगे जो अक्सर Indian English बोलते हैं
        target_names = ["Neerja", "Prabhat", "Aditi", "Kajal", "Arjun", "Raveena", "Devi", "Manish"]
        
        found = False
        print(f"\n{'Voice ID':<35} | {'Name':<15} | {'Language':<20}")
        print("-" * 80)

        for voice in data:
            name = voice.get("name", "")
            # अगर नाम हमारे target list में है
            if any(target in name for target in target_names):
                found = True
                print(f"{voice['voice_id']:<35} | {name:<15} | {voice.get('language')}")
        
        if not found:
            print("\nCould not find specific names. Printing ANY English voice to check format:")
            count = 0
            for voice in data:
                if "English" in voice.get("language", ""):
                    print(f"{voice['voice_id']:<35} | {voice['name']:<15} | {voice['language']}")
                    count += 1
                    if count >= 5: break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_specific_voices()