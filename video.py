# =========================================================
# video.py (AUTO DEFAULT ENTERPRISE VERSION)
# =========================================================

import os
import requests
from dotenv import load_dotenv
from typing import Optional
import time

# ==============================
# LOAD ENV
# ==============================
load_dotenv()

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
HEYGEN_ENABLED = bool(HEYGEN_API_KEY)

BASE_URL = "https://api.heygen.com/v2"
BASE_URL_STATUS = "https://api.heygen.com/v1"

HEADERS = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json"
} if HEYGEN_ENABLED else {}

# ==============================
# DEFAULT SETTINGS  IMPORTANT)
# ==============================
DEFAULT_VOICE_ID = "35b5ede5ab804f0280fa406752c88eb3"   # Solemn Sachin
DEFAULT_AVATAR_ID = "2892cad60dc54079b72cdc6bdff6eda6"

TEMPLATE_ID = "8aac65f3029b434e974403ca040f82fe"


# =========================================================
# AUTO SPEED LOGIC
# =========================================================
def calculate_speed(text: str) -> float:
    length = len(text)

    if length > 1500:
        return 1.25
    elif length > 1000:
        return 1.2
    elif length > 600:
        return 1.15
    else:
        return 1.0


# =========================================================
# GENERATE TEMPLATE VIDEO (AUTO DEFAULT ENABLED)
# =========================================================
def generate_template_video(
    text: str,
    voice_id: Optional[str] = None,
    avatar_id: Optional[str] = None,
    title: str = "AskDoubt-AI-Video"
) -> str:

    if not HEYGEN_ENABLED:
        raise RuntimeError("HEYGEN_API_KEY missing")

    if not text:
        raise ValueError("text is required")

    #  AUTO DEFAULT APPLY
    voice_id = voice_id or DEFAULT_VOICE_ID
    avatar_id = avatar_id or DEFAULT_AVATAR_ID

    speed = calculate_speed(text)

    payload = {
        "template_id": TEMPLATE_ID,
        "title": title[:120],
        "caption": True,
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id
                },
                "voice": {
                    "type": "text",
                    "voice_id": voice_id,
                    "input_text": text[:2000],
                    "speed": speed
                }
            }
        ],
        "template_variables": {
            "script_0": text[:2000]
        }
    }

    try:
        res = requests.post(
            f"{BASE_URL}/video/generate",
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        if res.status_code != 200:
            raise RuntimeError(f"HeyGen generate error: {res.text}")

        data = res.json().get("data", {})
        video_id = data.get("video_id")

        if not video_id:
            raise RuntimeError(f"No video_id returned: {res.text}")

        print(" Video created:", video_id)
        print(" Voice used:", voice_id)
        print(" Avatar used:", avatar_id)
        print(" Speed:", speed)

        return video_id

    except Exception as e:
        raise RuntimeError(f"Video generation failed: {str(e)}")


# =========================================================
# GET VIDEO STATUS
# =========================================================
def get_video_status(video_id: str):

    if not HEYGEN_ENABLED:
        return {"status": "disabled", "video_url": None}

    try:
        res = requests.get(
            f"{BASE_URL_STATUS}/video_status.get",
            headers=HEADERS,
            params={"video_id": video_id},
            timeout=15
        )

        if res.status_code != 200:
            print("Status API Error:", res.text)
            return {"status": "processing", "video_url": None}

        data = res.json().get("data", {})
        status = data.get("status", "").lower()
        video_url = data.get("video_url")

        print("Current Status:", status)

        if status == "completed":
            return {"status": "completed", "video_url": video_url}

        if status == "failed":
            return {"status": "failed", "video_url": None}

        return {"status": "processing", "video_url": None}

    except Exception as e:
        print("STATUS ERROR:", e)
        return {"status": "processing", "video_url": None}


# =========================================================
# POLL UNTIL COMPLETE
# =========================================================
def poll_video(video_id: str) -> str | None:

    for attempt in range(60):  # max ~2 min

        result = get_video_status(video_id)
        status = result.get("status")
        video_url = result.get("video_url")

        print(f"[POLL] Attempt {attempt} | Status = {status}")

        if status == "completed" and video_url:
            print(" Video Ready")
            return video_url

        if status == "failed":
            print(" Video failed")
            return None

        time.sleep(2)

    print(" Poll timeout")
    return None