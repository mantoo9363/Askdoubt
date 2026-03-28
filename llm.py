#import os
#import time
#from dotenv import load_dotenv
#import google.generativeai as genai

# =====================================
# Load Environment
# =====================================
#load_dotenv()

#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.0-flash")

#if not GEMINI_API_KEY:
 #   raise RuntimeError("GEMINI_API_KEY missing in .env file")

# Configure Gemini
#genai.configure(api_key=GEMINI_API_KEY)

# Create Model Object
#model = genai.GenerativeModel(MODEL_NAME)

#MAX_WORDS = 110


# =====================================
# Utility: Clean Text
# =====================================
#def clean_text(text: str) -> str:
 #   text = text.replace("\n", " ")
  #  text = " ".join(text.split())
   # return text.strip()


# =====================================
# Generate Response
# =====================================
#def generate_response(
 #   query: str,
  #  language: str,
   # grade: str,
    #subject: str,
    #mode: str ="explain"
#) -> str:
 #   if not query or not query.strip():
  #      return "Please ask a valid question."

    #  Mode-based limits (prompt same rahega)
   # if mode == "voice":
    #    max_words = 40        # 15–25 sec video
     #   max_tokens = 120
    #elif mode == "explain":
     #   max_words = 100
      #  max_tokens = 220
    #else:
     #   max_words = 200
      #  max_tokens = 300

    #prompt = f"""
    #You are a friendly and professional Indian school teacher.

    #Student Details:
    #- Class: {grade}
    #- Subject: {subject}
    #- Language: {language}

    #Adjust teaching difficulty based on class level:

    #Class 1–2:
    #Use very simple words, very short sentences, and fun daily-life examples.

    #Class 3–5:
    #Explain in simple language with one easy example.

    #Class 6–8:
    #Explain step-by-step with clear examples.

    #Class 9–10:
    #Explain clearly using important terms and one practical example.

    #Class 11–12:
    #Provide concept clarity with deeper explanation and real-world application.

    #Teaching Rules:
    #- Use simple Indian English.
    #- Keep explanation easy to understand.
    #- Use one relatable real-life example.
    #- If the subject is:
     #   Math → Show steps clearly.
     #   Science → Explain concept and why it happens.
      #  Social Studies → Use simple facts and context.
       # English → Explain meaning with examples.

    #Mode: {mode}

    #If mode = "explain":
    #Give a clear explanation in 80–120 words.

    #If mode = "quiz":
    #Create:
    #- 3 Multiple Choice Questions
    #- 1 Short Answer Question
    #- 1 True/False Question

    #If mode = "homework":
    #Create:
    #- 5 practice questions
    #- One application-based question

    #If mode = "voice":
    #Explain in a conversational classroom tone suitable for speaking.

    #Student Question / Topic:
    #{query}
    #"""

   # response = model.generate_content(
    #    prompt,
     #   generation_config=genai.types.GenerationConfig(
      #      temperature=0.4,
       #     max_output_tokens=max_tokens
       # )
    #)

    #if not response or not hasattr(response, "text") or not response.text:
     #   return "AI is BusY Right Now please Try after some time."

   # text = clean_text(response.text)

    # Strict word trimming
   # words = text.split()
    #if len(words) > max_words:
     #   text = " ".join(words[:max_words])

    #return text


#========================new code llm modeel and prompt------27 mar 2025===============

import os
from dotenv import load_dotenv
import google.generativeai as genai

# =====================================
# LOAD ENV
# =====================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# =====================================
# ALLOWED TYPES
# =====================================
ALLOWED_TYPES = {
    "academic",
    "skill",
    "entrepreneurship",
    "competitive",
    "ielts",
    "french",
    "arabic",
    "sanskrit",
    "german",
    "spanish"
}

# =====================================
# CLEAN TEXT
# =====================================
def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text.strip()

# =====================================
# LANGUAGE PROMPT
# =====================================
def get_language_prompt(query: str, lang: str):

    if lang == "ielts":
        return f"""
You are an IELTS English trainer.

1. Correct the sentence
2. Give better version
3. Explain mistakes simply
4. Give 2 example sentences

User Sentence:
{query}
"""

    return f"""
You are a language tutor.

Target Language: {lang}

Instructions:
1. Translate sentence
2. Give pronunciation (simple)
3. Explain meaning
4. Give 2 examples
5. Ask one practice question

User Input:
{query}
"""

# =====================================
# MAIN FUNCTION
# =====================================
def generate_response(
    query: str,
    language: str = "en",
    grade: str = "",
    subject: str = "",
    mode: str = "explain",
    llm_type: str = "academic"
) -> str:

    if not query or not query.strip():
        return "Please ask a valid question."

    llm_type = llm_type.lower()

    # =========================
    # VALIDATION
    # =========================
    if llm_type not in ALLOWED_TYPES:
        return "Invalid type selected."

    # =========================
    # MODE LIMITS
    # =========================
    if mode == "voice":
        max_words = 40
        max_tokens = 120
    elif mode == "explain":
        max_words = 100
        max_tokens = 220
    else:
        max_words = 200
        max_tokens = 300

    # =========================
    #  LANGUAGE TYPES
    # =========================
    if llm_type in {"ielts", "french", "arabic", "sanskrit", "german", "spanish"}:
        prompt = get_language_prompt(query, llm_type)

    # =========================
    # 🎓 ACADEMIC
    # =========================
    elif llm_type == "academic":

        prompt = f"""
You are a friendly Indian school teacher.

Class: {grade}
Subject: {subject}

Explain clearly with one example.
Keep it simple.

Mode: {mode}

Question:
{query}
"""

    # =========================
    # 💻 SKILL
    # =========================
    elif llm_type == "skill":

        prompt = f"""
You are a practical mentor.

- Give step-by-step answer
- Focus on real-world usage

User Query:
{query}
"""

    # =========================
    # 🚀 ENTREPRENEURSHIP
    # =========================
    elif llm_type == "entrepreneurship":

        prompt = f"""
You are a startup mentor.

- Give practical business ideas
- Explain steps

User Query:
{query}
"""

    # =========================
    #  COMPETITIVE
    # =========================
    elif llm_type == "competitive":

        prompt = f"""
You are a competitive exam teacher.

- Focus on important points
- Keep answer short

Question:
{query}
"""

    else:
        return "Invalid mode."

    # =========================
    # CALL GEMINI
    # =========================
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=max_tokens
            )
        )

        if not response or not hasattr(response, "text") or not response.text:
            return "AI is busy, please try again."

        text = clean_text(response.text)

        # WORD LIMIT
        words = text.split()
        if len(words) > max_words:
            text = " ".join(words[:max_words])

        return text

    except Exception as e:
        print("LLM Error:", str(e))
        return "Something went wrong."







#=============================nedw code section end====================================