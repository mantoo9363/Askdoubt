# ==============================================
# main.py (Enterprise Production Version - FINAL)
# ==============================================

from fastapi import (
    FastAPI, HTTPException,
    BackgroundTasks, Request
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response as FastAPIResponse
from starlette.middleware.base import BaseHTTPMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import os
import logging
import requests
# ==============================
# INTERNAL IMPORTS
# ==============================
import razorpay
from models import UserQuery, Response,Language,CreateOrder, VerifyPayment  
from rag import store_query
from llm import generate_response
from video import generate_template_video, poll_video
from database import get_db, init_db
from script import transcribe_audio_local
from fastapi import UploadFile, File, Form
import tempfile
from typing import Optional

from dotenv import load_dotenv
load_dotenv()
# ==============================
# ENV CONFIG
# ==============================
ENV = os.getenv("ENV", "dev")

# ==============================
# RAZORPAY CONFIG
# ==============================



RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

# ==============================
# LOGGING
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
# APP INIT
# ==============================
app = FastAPI(
    title="Ask Doubt AI - Enterprise Secure",
    docs_url="/docs" if ENV == "dev" else None,
    redoc_url=None
)

# ==============================
# STARTUP
# ==============================
@app.on_event("startup")
def startup():
    init_db()
    logger.info("Database Initialized Successfully")

   

# ==============================
# CORS (Dev Mode Safe)
# ==============================

#ALLOWED_ORIGINS = [
 #   "https://theteachly.com",      # Allow the main apex domain
  #  "https://*.theteachly.com",  # Keep allowing all subdomains
#]

ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
#app.add_middleware(
 #   CORSMiddleware,
  #  allow_origins=ALLOWED_ORIGINS,
   # allow_credentials=True,
    #allow_methods=["POST", "GET"],
    #allow_headers=["*"],
#)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# SECURITY HEADERS
# ==============================
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "no-referrer"
        # Allow Swagger UI/ReDoc to load external and inline resources
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "  # Default to self
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "  # Allow inline scripts and CDN
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "   # Allow inline styles and CDN
            "img-src 'self' data:;"  # Allow data URIs for images (like favicons)
        )

        return response

app.add_middleware(SecurityHeadersMiddleware)

# ==============================
# RATE LIMITER
# ==============================
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
#app.add_exception_handler(RateLimitExceeded, limiter._rate_limit_exceeded_handler)
# =========================================================
# BACKGROUND VIDEO POLLING
# =========================================================
def process_video_background(video_id: str):
    try:
        video_url = poll_video(video_id)
        if not video_url:
            return

        with get_db() as conn:
            conn.execute(
                "UPDATE queriesnew SET video_url=? WHERE video_id=?",
                (video_url, video_id)
            )
            conn.commit()

        logger.info(f"Video completed: {video_id}")

    except Exception as e:
        logger.error(f"Background video error: {e}")

# =========================================================
# ASK API
# =========================================================
# =========================================================
# ASK API (UPDATED ENTERPRISE VERSION)
# =========================================================
# =========================================================
# ASK API (WITHOUT MODE VERSION - CLEAN)
# =========================================================
# =========================================================
# ASK API (FINAL FIXED VERSION)
# =========================================================
@app.post("/ask", response_model=Response)
@limiter.limit("10/minute")
async def ask_doubt(
    request: Request,
    user_input: UserQuery,
    background_tasks: BackgroundTasks
):

    # ===============================
    # VALIDATION
    # ===============================
    if not user_input.query or not user_input.query.strip():
        raise HTTPException(status_code=400, detail="Query required")

    query = user_input.query.strip()

    language = (
        user_input.language.value
        if hasattr(user_input.language, "value")
        else user_input.language
    )

    grade = user_input.class_name or "Class 8"
    subject = user_input.subject_name or "Computer"
    chapter = user_input.chapter_name or "General"
    user_id = user_input.user_id or "user-1"

    mode = "voice" if user_input.input_type == "voice" else "explain"

    logger.info(f"Mode selected: {mode}")

    # ===============================
    # CHECK USER CREDITS
    # ===============================
    with get_db() as conn:

        credit_row = conn.execute(
            """
            SELECT balance
            FROM credits
            WHERE user_id=?
            """,
            (user_id,)
        ).fetchone()

        if not credit_row or credit_row["balance"] <= 0:
            return Response(
                text="Credit is not available. Please buy credits.",
                video_url=None,
                video_id=None,
                video_status="none",
                is_retrieved=False,
                query_id=None,
                class_name=grade,
                subject_name=subject,
                chapter_name=chapter,
                download_url=None
            )

    # ===============================
    # CHECK EXISTING RECORD
    # ===============================
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT id, response_text, video_url
            FROM queriesnew
            WHERE query_text=? 
            AND language=? 
            AND class_name=? 
            AND subject_name=? 
            ORDER BY id DESC
            LIMIT 1
            """,
            (query, language, grade, subject)
        ).fetchone()

    if row:
        return Response(
            text=row[1],
            video_url=row[2],
            video_status="completed" if row[2] else "none",
            is_retrieved=True,
            query_id=row[0],
            class_name=grade,
            subject_name=subject,
            chapter_name=chapter,
            download_url=f"/download/{row[0]}" if row[2] else None
        )

    # ===============================
    # GENERATE AI RESPONSE
    # ===============================
    logger.info("Calling LLM...")

    text = await run_in_threadpool(
        generate_response,
        query,
        language,
        grade,
        subject,
        mode
    )

    logger.info("LLM response generated")

    if not text:
        raise HTTPException(status_code=500, detail="AI generation failed")

    text = " ".join(text.split())[:800]

    video_id = None

    # ===============================
    # GENERATE VIDEO
    # ===============================
    try:
        logger.info("Generating HeyGen Video...")

        video_id = await run_in_threadpool(
            generate_template_video,
            text,
            user_input.voice_id,
            user_input.avatar_id
        )

        logger.info(f"Video ID created: {video_id}")

    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        video_id = None

    # ===============================
    # SAVE TO DATABASE
    # ===============================
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO queriesnew
            (user_id,query_text,response_text,video_url,language,video_id,
             class_name,subject_name,chapter_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                query,
                text,
                None,
                language,
                video_id,
                grade,
                subject,
                chapter
            )
        )

        # ===============================
        # DEDUCT CREDIT
        # ===============================
        conn.execute(
            """
            UPDATE credits
            SET usedcredits = usedcredits + 1,
                balance = balance - 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id=? AND balance > 0
            """,
            (user_id,)
        )

        conn.commit()

        query_id = cursor.lastrowid

    # Background polling
    if video_id:
        background_tasks.add_task(process_video_background, video_id)

    # Store in RAG
    await run_in_threadpool(store_query, query, text, "", language)

    # ===============================
    # RETURN RESPONSE
    # ===============================
    return Response(
        text=text,
        video_url=None,
        video_id=video_id,
        video_status="processing" if video_id else "none",
        is_retrieved=False,
        query_id=query_id,
        class_name=grade,
        subject_name=subject,
        chapter_name=chapter,
        download_url=f"/download/{query_id}" if video_id else None
    )
# =========================================================
# VIDEO STATUS ENDPOINT ( REQUIRED FOR WIDGET)
# =========================================================
@app.get("/video-status/{video_id}")
def video_status(video_id: str):
    with get_db() as conn:
        row = conn.execute(
            "SELECT video_url FROM queriesnew WHERE video_id=?",
            (video_id,)
        ).fetchone()

    if row and row[0]:
        return {"status": "completed", "video_url": row[0]}

    return {"status": "processing", "video_url": None}
# =========================================================
# DOWNLOAD ENDPOINT
# =========================================================
@app.get("/download/{video_id}")
def download_video(video_id: str):

    with get_db() as conn:
        row = conn.execute(
            "SELECT video_url FROM queriesnew WHERE video_id=?",
            (video_id,)
        ).fetchone()

    if not row or not row[0]:
        raise HTTPException(status_code=404, detail="Video not ready yet")

    res = requests.get(row[0], stream=True, timeout=180)
    res.raise_for_status()

    return FastAPIResponse(
        content=res.content,
        media_type="video/mp4",
        headers={
            "Content-Disposition": f'attachment; filename=\"{video_id}.mp4\"'
        }
    )


# =========================================================
# VOICE API
# =========================================================
@app.post("/voice", response_model=Response)
@limiter.limit("5/minute")
async def handle_voice(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = Form("en")
):

    #  Save with correct extension (webm)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        query = transcribe_audio_local(tmp_path)

        #  Convert string → Enum safely
        try:
            lang_enum = Language(language)
        except ValueError:
            lang_enum = Language.EN

        voice_user_input = UserQuery(
            query=query,
            language=lang_enum
        )

        return await ask_doubt(request, voice_user_input, background_tasks)

    finally:
        os.unlink(tmp_path)

# =========================================================


@app.post("/create-order")
async def create_order(data: CreateOrder):

    try:

        order = razorpay_client.order.create({

            "amount": data.amount * 100,
            "currency": "INR",
            "payment_capture": 1

        })

        return {

            "order_id": order["id"],
            "amount": order["amount"],
            "credits": data.credits,
            "user_id": data.user_id

        }

    except Exception as e:

        logger.error(f"Order creation failed: {e}")

        raise HTTPException(status_code=500, detail="Order creation failed")
    


    # =========================================================
# VERIFY PAYMENT + ADD CREDITS
# =========================================================
@app.post("/verify-payment")
async def verify_payment(data: VerifyPayment):

    params = {

        "razorpay_order_id": data.razorpay_order_id,
        "razorpay_payment_id": data.razorpay_payment_id,
        "razorpay_signature": data.razorpay_signature
    }

    try:

        razorpay_client.utility.verify_payment_signature(params)

        with get_db() as conn:

            cursor = conn.cursor()

            # Check existing credits
            row = cursor.execute(

                "SELECT totalcredits,usedcredits FROM credits WHERE user_id=?",

                (data.user_id,)

            ).fetchone()

            if row:

                total = row["totalcredits"] + data.credits
                used = row["usedcredits"]
                balance = total - used

                cursor.execute("""

                UPDATE credits
                SET totalcredits=?,
                    balance=?,
                    updated_at=CURRENT_TIMESTAMP
                WHERE user_id=?

                """,(total,balance,data.user_id))

            else:

                total = data.credits
                used = 0
                balance = data.credits

                cursor.execute("""

                INSERT INTO credits
                (user_id,totalcredits,usedcredits,balance)

                VALUES(?,?,?,?)

                """,(data.user_id,total,used,balance))


            # Payment history

            cursor.execute("""

            INSERT INTO payments
            (user_id,credits,usedcredits,balance,payment_id,amount)

            VALUES(?,?,?,?,?,?)

            """,(data.user_id,data.credits,used,balance,
                 data.razorpay_payment_id,data.amount))

            conn.commit()

        return {

            "status": "success",
            "credits_added": data.credits,
            "balance": balance

        }

    except Exception as e:

        logger.error(f"Payment verification failed: {e}")

        raise HTTPException(status_code=400, detail="Payment verification failed")


#============================payment history===================================
#=========================== CREDIT WALLET =======================================

@app.get("/credit-history/{user_id}")
def credit_history(user_id: str):

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT 
                credits_added,
                credits_used,
                balance,
                created_at
            FROM credit_history
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(r) for r in rows]
#=============================================================================

#===========================credit history===========================================

#============================ PAYMENT HISTORY ===================================

@app.get("/payment-history/{user_id}")
def payment_history(user_id: str):

    try:
        with get_db() as conn:
            rows = conn.execute(
                """
                SELECT 
                    id,
                    amount,
                    credits,
                    usedcredits,
                    balance,
                    payment_id,
                    created_at
                FROM payments
                WHERE user_id=?
                ORDER BY id DESC
                """,
                (user_id,)
            ).fetchall()

        return [dict(r) for r in rows]

    except Exception as e:
        return {"error": str(e)}


#========================================================================================


# =========================================================
# HEALTH CHECK
# =========================================================
@app.get("/health")
def health():
    return {"status": "running"}

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)