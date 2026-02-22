# ==============================================
# main.py (Enterprise Production Version - FINAL)
# ==============================================

from fastapi import (
    FastAPI, HTTPException,
    BackgroundTasks, Request
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import os
import logging

# ==============================
# INTERNAL IMPORTS
# ==============================
from models import UserQuery, Response,Language  
from rag import store_query
from llm import generate_response
from video import generate_template_video, poll_video
from database import get_db, init_db
from script import transcribe_audio_local
from fastapi import UploadFile, File, Form
import tempfile

# ==============================
# ENV CONFIG
# ==============================
ENV = os.getenv("ENV", "dev")

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev ke liye
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
        response.headers["Referrer-Policy"] = "no-referrer"

        return response

app.add_middleware(SecurityHeadersMiddleware)

# ==============================
# RATE LIMITER
# ==============================
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
@app.post("/ask", response_model=Response)
@limiter.limit("10/minute")
async def ask_doubt(
    request: Request,
    user_input: UserQuery,
    background_tasks: BackgroundTasks
):

    if not user_input.query or not user_input.query.strip():
        raise HTTPException(status_code=400, detail="Query required")

    query = user_input.query.strip()
    language = user_input.language.value

    # ===============================
    # CHECK EXISTING RECORD
    # ===============================
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT response_text, video_url
            FROM queriesnew
            WHERE query_text=? AND language=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (query, language)
        ).fetchone()

    if row:
        return Response(
            text=row[0],
            video_url=row[1],
            is_retrieved=True,
            video_status="completed" if row[1] else "none",
            video_id=None,
            download_url=None
        )

    # ===============================
    # GENERATE AI TEXT
    # ===============================
    text = await run_in_threadpool(generate_response, query, language)

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
            text
        )

        logger.info(f"Video ID: {video_id}")

        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO queriesnew
                (query_text, response_text, video_url, language, video_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (query, text, None, language, video_id)
            )
            conn.commit()

        background_tasks.add_task(process_video_background, video_id)

    except Exception as e:
        logger.error(f"Video generation failed: {e}")

    await run_in_threadpool(store_query, query, text, "", language)

    return Response(
        text=text,
        video_url=None,
        is_retrieved=False,
        video_status="processing" if video_id else "none",
        video_id=video_id,
        download_url=f"/download/{video_id}" if video_id else None
    )

# =========================================================
# VIDEO STATUS ENDPOINT (🔥 REQUIRED FOR WIDGET)
# =========================================================
@app.get("/video-status/{video_id}")
def check_video_status(video_id: str):

    with get_db() as conn:
        row = conn.execute(
            "SELECT video_url FROM queriesnew WHERE video_id=?",
            (video_id,)
        ).fetchone()

    if not row:
        return {"status": "processing"}

    video_url = row[0]

    if video_url:
        return {
            "status": "completed",
            "video_url": video_url
        }

    return {"status": "processing"}

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
        raise HTTPException(status_code=404, detail="Video not ready")

    return RedirectResponse(row[0])


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