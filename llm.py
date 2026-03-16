import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# =====================================
# Load Environment
# =====================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create Model Object
model = genai.GenerativeModel(MODEL_NAME)

MAX_WORDS = 110


# =====================================
# Utility: Clean Text
# =====================================
def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text.strip()


# =====================================
# Generate Response
# =====================================
def generate_response(
    query: str,
    language: str,
    grade: str,
    subject: str,
    mode: str ="explain"
) -> str:
    if not query or not query.strip():
        return "Please ask a valid question."

    # 🔥 Mode-based limits (prompt same rahega)
    if mode == "voice":
        max_words = 40        # 15–25 sec video
        max_tokens = 120
    elif mode == "explain":
        max_words = 100
        max_tokens = 220
    else:
        max_words = 200
        max_tokens = 300

    prompt = f"""
    You are a friendly and professional Indian school teacher.

    Student Details:
    - Class: {grade}
    - Subject: {subject}
    - Language: {language}

    Adjust teaching difficulty based on class level:

    Class 1–2:
    Use very simple words, very short sentences, and fun daily-life examples.

    Class 3–5:
    Explain in simple language with one easy example.

    Class 6–8:
    Explain step-by-step with clear examples.

    Class 9–10:
    Explain clearly using important terms and one practical example.

    Class 11–12:
    Provide concept clarity with deeper explanation and real-world application.

    Teaching Rules:
    - Use simple Indian English.
    - Keep explanation easy to understand.
    - Use one relatable real-life example.
    - If the subject is:
        Math → Show steps clearly.
        Science → Explain concept and why it happens.
        Social Studies → Use simple facts and context.
        English → Explain meaning with examples.

    Mode: {mode}

    If mode = "explain":
    Give a clear explanation in 80–120 words.

    If mode = "quiz":
    Create:
    - 3 Multiple Choice Questions
    - 1 Short Answer Question
    - 1 True/False Question

    If mode = "homework":
    Create:
    - 5 practice questions
    - One application-based question

    If mode = "voice":
    Explain in a conversational classroom tone suitable for speaking.

    Student Question / Topic:
    {query}
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=max_tokens
        )
    )

    if not response or not hasattr(response, "text") or not response.text:
        return "AI is BusY Right Now please Try after some time."

    text = clean_text(response.text)

    # Strict word trimming
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words])

    return text