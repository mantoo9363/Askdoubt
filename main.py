# ==============================================
# main.py (Enterprise Production Version - FINAL)
# ==============================================

#from fastapi import (
 #   FastAPI, HTTPException,
  #  BackgroundTasks, Request
#)
#from fastapi.middleware.cors import CORSMiddleware
#from fastapi.concurrency import run_in_threadpool
#from fastapi.responses import Response as FastAPIResponse
#from starlette.middleware.base import BaseHTTPMiddleware

#from slowapi import Limiter
#from slowapi.util import get_remote_address
#from slowapi.errors import RateLimitExceeded

#import os
#import logging
#import requests
# ==============================
# INTERNAL IMPORTS
# ==============================
#import razorpay
#from models import UserQuery, Response,Language,CreateOrder, VerifyPayment  
#from rag import store_query
#from llm import generate_response
#from video import generate_template_video, poll_video
#from database import get_db, init_db
#from script import transcribe_audio_local
#from fastapi import UploadFile, File, Form
#import tempfile
#from typing import Optional
#import base64

#from dotenv import load_dotenv
#load_dotenv()
# ==============================
# ENV CONFIG
# ==============================
#ENV = os.getenv("ENV", "dev")

# ==============================
# RAZORPAY CONFIG
# ==============================



#RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
#RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

#razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

# ==============================
# LOGGING
# ==============================
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

# ==============================
# APP INIT
# ==============================
#app = FastAPI(
 #   title="Ask Doubt AI - Enterprise Secure",
  #  docs_url="/docs" if ENV == "dev" else None,
   # redoc_url=None
#)

# ==============================
# STARTUP
# ==============================
#@app.on_event("startup")
#def startup():
 #   init_db()
  #  logger.info("Database Initialized Successfully")

   

# ==============================
# CORS (Dev Mode Safe)
# ==============================

#ALLOWED_ORIGINS = [
 #   "https://theteachly.com",
  #  "https://student.theteachly.com",
   # "https://credits.theteachly.com",  
#]
#ALLOWED_ORIGINS = [
  #  "http://localhost:5500",
   # "http://127.0.0.1:5500",
#]


#app.add_middleware(
 #   CORSMiddleware,
  #  allow_origins=["*"],   
   # allow_credentials=True,
    #allow_methods=["*"],
    #allow_headers=["*"],
#)
# ==============================
# SECURITY HEADERS
# ==============================
#class SecurityHeadersMiddleware(BaseHTTPMiddleware):
 #   async def dispatch(self, request: Request, call_next):
  #      response = await call_next(request)

   #     response.headers["X-Content-Type-Options"] = "nosniff"
    #    response.headers["X-Frame-Options"] = "DENY"
     #   response.headers["X-XSS-Protection"] = "1; mode=block"
      #  response.headers["Referrer-Policy"] = "no-referrer"
       # # Allow Swagger UI/ReDoc to load external and inline resources
        #response.headers["Content-Security-Policy"] = (
         #   "default-src 'self'; "  # Default to self
          #  "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "  # Allow inline scripts and CDN
           # "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "   # Allow inline styles and CDN
            #"img-src 'self' data:;"  # Allow data URIs for images (like favicons)
        #)

        #return response

#app.add_middleware(SecurityHeadersMiddleware)

# ==============================
# RATE LIMITER
# ==============================
#limiter = Limiter(key_func=get_remote_address)
#app.state.limiter = limiter
#app.add_exception_handler(RateLimitExceeded, limiter._rate_limit_exceeded_handler)
# =========================================================
# BACKGROUND VIDEO POLLING
# =========================================================
#def process_video_background(video_id: str):
 #   try:
  #      video_url = poll_video(video_id)
   #     if not video_url:
    #        return

#        with get_db() as conn:
 #           conn.execute(
  #              "UPDATE queriesnew SET video_url=? WHERE video_id=?",
   #             (video_url, video_id)
    #        )
     #       conn.commit()

      #  logger.info(f"Video completed: {video_id}")

    #except Exception as e:
     #   logger.error(f"Background video error: {e}")

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
#@app.post("/ask", response_model=Response)
#@limiter.limit("10/minute")
#async def ask_doubt(
 #   request: Request,
  #  user_input: UserQuery,
   # background_tasks: BackgroundTasks
#):

    # ===============================
    # VALIDATION
    # ===============================
 #   if not user_input.query or not user_input.query.strip():
  #      raise HTTPException(status_code=400, detail="Query required")

   # query = user_input.query.strip()

   # language = (
    #    user_input.language.value
     #   if hasattr(user_input.language, "value")
      #  else user_input.language
    #)

    #grade = user_input.class_name or "Class 8"
    #subject = user_input.subject_name or "Computer"
    #chapter = user_input.chapter_name or "General"

    # ===============================
    # DECODE USER ID (IMPORTANT )
    # ===============================
   # raw_user_id = user_input.user_id or "guest_user"

   # try:
    #    user_id = base64.b64decode(raw_user_id).decode("utf-8")
    #except Exception:
     #   user_id = raw_user_id  # fallback

    #logger.info(f"User: {user_id}")

    #mode = "voice" if user_input.input_type == "voice" else "explain"

    # ===============================
    # ENSURE USER EXISTS IN CREDITS
    # ===============================
    #with get_db() as conn:
     #   conn.execute(
      #      """
       #     INSERT OR IGNORE INTO credits (user_id, balance, usedcredits)
        #    VALUES (?, 0, 0)
         #   """,
          #  (user_id,)
        #)
        #conn.commit()

    # ===============================
    # CHECK USER CREDITS
    # ===============================
    #with get_db() as conn:
     #   credit_row = conn.execute(
      #      """
       #     SELECT balance
        #    FROM credits
         #   WHERE user_id=?
          #  """,
           # (user_id,)
        #).fetchone()

        #if not credit_row or credit_row["balance"] <= 0:
         #   return Response(
          #      text=" Credit not available. Please buy credits.",
           #     video_url=None,
            #    video_id=None,
             #   video_status="none",
              #  is_retrieved=False,
               # query_id=None,
                #class_name=grade,
                #subject_name=subject,
                #chapter_name=chapter,
                #download_url=None
            #)

    # ===============================
    # CHECK EXISTING QUERY
    # ===============================
    #with get_db() as conn:
     #   row = conn.execute(
      #      """
       #     SELECT id, response_text, video_url
        #    FROM queriesnew
         #   WHERE query_text=? 
          #  AND language=? 
           # AND class_name=? 
          #  AND subject_name=? 
          #  ORDER BY id DESC
          #  LIMIT 1
           # """,
           # (query, language, grade, subject)
        #).fetchone()

    #if row:
     #   return Response(
      #      text=row[1],
       #     video_url=row[2],
        #    video_status="completed" if row[2] else "none",
         #   is_retrieved=True,
          #  query_id=row[0],
         #   class_name=grade,
          #  subject_name=subject,
          #  chapter_name=chapter,
          #  download_url=f"/download/{row[0]}" if row[2] else None
      #  )

    # ===============================
    # GENERATE AI RESPONSE
    # ===============================
   # logger.info("Calling LLM...")

   # text = await run_in_threadpool(
    #    generate_response,
     #   query,
      #  language,
       # grade,
        #subject,
       # mode
   # )

   # if not text:
    #    raise HTTPException(status_code=500, detail="AI generation failed")

   # text = " ".join(text.split())[:800]

   # video_id = None

    # ===============================
    # GENERATE VIDEO
    # ===============================
  #  try:
   #     logger.info("Generating video...")

    #    video_id = await run_in_threadpool(
     #       generate_template_video,
      #      text,
       #     user_input.voice_id,
        #    user_input.avatar_id
       # )

   # except Exception as e:
    #    logger.error(f"Video generation failed: {e}")
     #   video_id = None

    # ===============================
    # SAVE + DEDUCT CREDIT (SAFE)
    # ===============================
  #  with get_db() as conn:

   #     cursor = conn.execute(
    #        """
     #       INSERT INTO queriesnew
      #      (user_id, query_text, response_text, video_url, language, video_id,
       #      class_name, subject_name, chapter_name)
        #    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
         #   """,
          #  (
           #     user_id,
            #    query,
             #   text,
              #  None,
             #   language,
             #   video_id,
              #  grade,
              #  subject,
              #  chapter
           # )
       # )

        # SAFE CREDIT DEDUCTION
       # updated = conn.execute(
        #    """
         #   UPDATE credits
          #  SET usedcredits = usedcredits + 1,
           #     balance = balance - 1,
            #    updated_at = CURRENT_TIMESTAMP
          #  WHERE user_id=? AND balance > 0
          #  """,
          #  (user_id,)
      #  )

       # if updated.rowcount == 0:
        #    conn.rollback()
         #   return Response(
          #      text=" Credit exhausted. Please recharge.",
           #     video_url=None,
            #    video_id=None,
             #   video_status="none",
            #    is_retrieved=False,
             #   query_id=None,
              #  class_name=grade,
               # subject_name=subject,
                #chapter_name=chapter,
               # download_url=None
          #  )

       # conn.commit()

      #  query_id = cursor.lastrowid

    # ===============================
    # BACKGROUND VIDEO PROCESS
    # ===============================
   # if video_id:
    #    background_tasks.add_task(process_video_background, video_id)

    # ===============================
    # STORE IN RAG
    # ===============================
   # await run_in_threadpool(store_query, query, text, "", language)

    # ===============================
    # RESPONSE
    # ===============================
  #  return Response(
   #     text=text,
    #    video_url=None,
     #   video_id=video_id,
      #  video_status="processing" if video_id else "none",
     #   is_retrieved=False,
     #   query_id=query_id,
     #   class_name=grade,
     #   subject_name=subject,
     #   chapter_name=chapter,
     #   download_url=f"/download/{query_id}" if video_id else None
   # )
# =========================================================
# VIDEO STATUS ENDPOINT ( REQUIRED FOR WIDGET)
# =========================================================
#@app.get("/video-status/{video_id}")
#def video_status(video_id: str):
 #   with get_db() as conn:
  #      row = conn.execute(
   #         "SELECT video_url FROM queriesnew WHERE video_id=?",
    #        (video_id,)
     #   ).fetchone()

  #  if row and row[0]:
   #     return {"status": "completed", "video_url": row[0]}

   # return {"status": "processing", "video_url": None}
# =========================================================
# DOWNLOAD ENDPOINT
# =========================================================
#@app.get("/download/{video_id}")
#def download_video(video_id: str):

 #   with get_db() as conn:
  #      row = conn.execute(
   #         "SELECT video_url FROM queriesnew WHERE video_id=?",
    #        (video_id,)
     #   ).fetchone()

  #  if not row or not row[0]:
   #     raise HTTPException(status_code=404, detail="Video not ready yet")

  #  res = requests.get(row[0], stream=True, timeout=180)
   # res.raise_for_status()

   # return FastAPIResponse(
    #    content=res.content,
     #   media_type="video/mp4",
     #   headers={
      #      "Content-Disposition": f'attachment; filename=\"{video_id}.mp4\"'
     #   }
  #  )


# =========================================================
# VOICE API
# =========================================================
#@app.post("/voice", response_model=Response)
#@limiter.limit("5/minute")
#async def handle_voice(
 #   request: Request,
  #  background_tasks: BackgroundTasks,
   # file: UploadFile = File(...),
  #  language: str = Form("en")
#):

    # Save file
 #   with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
  #      tmp.write(await file.read())
   #     tmp_path = tmp.name

   # try:
        #  FIX: transcription safe handling
    #    try:
     #       query = transcribe_audio_local(tmp_path)
      #  except Exception as e:
       #     return Response(
        #        text=f"Voice processing failed: {str(e)}",
         #       video_url=None,
          #      video_id=None,
           #     video_status="none",
            #    is_retrieved=False,
             #   query_id=None,
              #  class_name=None,
               # subject_name=None,
                #chapter_name=None,
               # download_url=None
           # )

        #if not query or not query.strip():
         #   return Response(
          #      text="Could not understand audio. Please try again.",
           #     video_url=None,
            #    video_id=None,
             #   video_status="none",
              #  is_retrieved=False,
               # query_id=None,
              #  class_name=None,
               # subject_name=None,
               # chapter_name=None,
               # download_url=None
           # )

        # Language handling
       # try:
        #    lang_enum = Language(language)
       # except ValueError:
        #    lang_enum = Language.EN

       # voice_user_input = UserQuery(
        #    query=query,
         #   language=lang_enum
       # )

       # return await ask_doubt(request, voice_user_input, background_tasks)

    #finally:
     #   os.unlink(tmp_path)
# =========================================================


#@app.post("/create-order")
#async def create_order(data: CreateOrder):

 #   try:

  #      order = razorpay_client.order.create({

   #         "amount": data.amount * 100,
    #        "currency": "INR",
     #       "payment_capture": 1

      #  })

       # return {

        #    "order_id": order["id"],
         #   "amount": order["amount"],
          #  "credits": data.credits,
         #   "user_id": data.user_id

      #  }

   # except Exception as e:

    #    logger.error(f"Order creation failed: {e}")

     #   raise HTTPException(status_code=500, detail="Order creation failed")
    


    # =========================================================
# VERIFY PAYMENT + ADD CREDITS
# =========================================================
#@app.post("/verify-payment")
#async def verify_payment(data: VerifyPayment):

 #   params = {

  #      "razorpay_order_id": data.razorpay_order_id,
   #     "razorpay_payment_id": data.razorpay_payment_id,
    #    "razorpay_signature": data.razorpay_signature
   # }

  #  try:

   #     razorpay_client.utility.verify_payment_signature(params)

    #    with get_db() as conn:

     #       cursor = conn.cursor()

            # Check existing credits
      #      row = cursor.execute(

       #         "SELECT totalcredits,usedcredits FROM credits WHERE user_id=?",

        #        (data.user_id,)

         #   ).fetchone()

          #  if row:

           #     total = row["totalcredits"] + data.credits
            #    used = row["usedcredits"]
             #   balance = total - used

              #  cursor.execute("""

               # UPDATE credits
              #  SET totalcredits=?,
               #     balance=?,
                #    updated_at=CURRENT_TIMESTAMP
              #  WHERE user_id=?

               # """,(total,balance,data.user_id))

           # else:

            #    total = data.credits
             #   used = 0
              #  balance = data.credits

               # cursor.execute("""

             #   INSERT INTO credits
              #  (user_id,totalcredits,usedcredits,balance)

               # VALUES(?,?,?,?)

               # """,(data.user_id,total,used,balance))


            # Payment history

           # cursor.execute("""

           # INSERT INTO payments
           # (user_id,credits,usedcredits,balance,payment_id,amount)

            #VALUES(?,?,?,?,?,?)

           # """,(data.user_id,data.credits,used,balance,
            #     data.razorpay_payment_id,data.amount))

            #conn.commit()

        #return {

         #   "status": "success",
          #  "credits_added": data.credits,
           # "balance": balance

      #  }

   # except Exception as e:

    #    logger.error(f"Payment verification failed: {e}")

     #   raise HTTPException(status_code=400, detail="Payment verification failed")


#============================payment history===================================
#=========================== CREDIT WALLET =======================================

#@app.get("/credit-history/{user_id}")
#def credit_history(user_id: str):

 #   try:
  #      with get_db() as conn:
   #         row = conn.execute(
    #            """
     #           SELECT totalcredits, usedcredits, balance
      #          FROM credits
       #         WHERE user_id=?
        #        """,
         #       (user_id,)
          #  ).fetchone()

       # if row:
        #    return dict(row)
       # else:
        #    return {
         #       "totalcredits": 0,
          #      "usedcredits": 0,
           #     "balance": 0
            #}

    #except Exception as e:
     #   print(" ERROR:", e)
      #  return {
       #     "error": str(e)
        #}
#=============================================================================

#===========================credit history===========================================

#============================ PAYMENT HISTORY ===================================

#@app.get("/payment-history/{user_id}")
#def payment_history(user_id: str):

 #   try:
  #      with get_db() as conn:
   #         rows = conn.execute(
    #            """
     #           SELECT 
      #              id,
       #             amount,
        #            credits,
         #           usedcredits,
          #          balance,
           #         payment_id,
            #        created_at
             #   FROM payments
              #  WHERE user_id=?
               # ORDER BY id DESC
               # """,
               # (user_id,)
            #).fetchall()

    #    return [dict(r) for r in rows]

   # except Exception as e:
    #    return {"error": str(e)}


#========================================================================================


# =========================================================
# HEALTH CHECK
# =========================================================
#@app.get("/health")
#def health():
 #   return {"status": "running"}

# =========================================================
# RUN
# =========================================================
#if __name__ == "__main__":
 #   import uvicorn
  #  uvicorn.run(app, host="0.0.0.0", port=9000)


#======================================new code 28 mar 2028===============================================
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import os
import logging
import razorpay
import base64
import tempfile

from models import UserQuery, Response, Language, CreateOrder, VerifyPayment
from rag import store_query
from llm import generate_response
from video import generate_template_video, poll_video
from database import get_db, init_db
from script import transcribe_audio_local

from dotenv import load_dotenv
load_dotenv()

# ==============================
# CONFIG
# ==============================
ENV = os.getenv("ENV", "dev")

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
# APP
# ==============================
app = FastAPI(
    title="Ask Doubt AI",
    docs_url="/docs" if ENV == "dev" else None,
    redoc_url=None
)

#  CORS (Production safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ENV == "dev" else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ==============================
# GLOBAL ERROR HANDLER
# ==============================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong"}
    )

# ==============================
# STARTUP
# ==============================
@app.on_event("startup")
def startup():
    init_db()
    logger.info("DB Initialized")

# ==============================
# VIDEO BACKGROUND
# ==============================
def process_video_background(video_id: str):
    try:
        video_url = poll_video(video_id)
        if video_url:
            with get_db() as conn:
                conn.execute(
                    "UPDATE queriesnew SET video_url=? WHERE video_id=?",
                    (video_url, video_id)
                )
                conn.commit()
    except Exception as e:
        logger.error(f"Video Background Error: {e}")

# ==============================
# ASK API
# ==============================
@app.post("/ask", response_model=Response)
@limiter.limit("10/minute")
async def ask_doubt(request: Request, user_input: UserQuery, background_tasks: BackgroundTasks):

    if not user_input.query:
        raise HTTPException(400, "Query required")

    query = user_input.query.strip()
    language = user_input.language.value

    llm_type = (
        user_input.llm_type.value
        if hasattr(user_input.llm_type, "value")
        else user_input.llm_type
    )

    grade = user_input.class_name or ""
    subject = user_input.subject_name or ""
    chapter = user_input.chapter_name or ""

    # Decode user
    try:
        user_id = base64.b64decode(user_input.user_id or "").decode()
    except:
        user_id = user_input.user_id or "guest"

    # =============================
    # CREDIT CHECK (SAFE)
    # =============================
    with get_db() as conn:
        row = conn.execute(
            "SELECT balance FROM credits WHERE user_id=?",
            (user_id,)
        ).fetchone()

        if not row:
            return Response(text="User not found")

        if row["balance"] <= 0:
            return Response(text="Buy credits first")

    # =============================
    # EXISTING CACHE
    # =============================
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT id, response_text, video_url
            FROM queriesnew
            WHERE query_text=? AND language=? AND llm_type=?
            ORDER BY id DESC LIMIT 1
            """,
            (query, language, llm_type)
        ).fetchone()

    if row:
        return Response(
            text=row["response_text"],
            video_url=row["video_url"],
            is_retrieved=True,
            llm_type=user_input.llm_type,
            query_id=row["id"]
        )

    # =============================
    # LLM CALL
    # =============================
    text = await run_in_threadpool(
        generate_response,
        query,
        language,
        grade,
        subject,
        "explain",
        llm_type
    )

    # =============================
    # VIDEO
    # =============================
    video_id = None
    try:
        video_id = await run_in_threadpool(
            generate_template_video,
            text,
            user_input.voice_id,
            user_input.avatar_id
        )
    except Exception as e:
        logger.error(f"Video error: {e}")

    # =============================
    # SAVE DB
    # =============================
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO queriesnew
            (user_id,name,email,mobile_number,
             query_text,response_text,language,llm_type,
             is_retrieved,video_id,class_name,subject_name,chapter_name)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                user_id,
                user_input.name,
                user_input.email,
                user_input.mobile_number,
                query,
                text,
                language,
                llm_type,
                0,
                video_id,
                grade,
                subject,
                chapter
            )
        )

        conn.execute(
            "UPDATE credits SET usedcredits=usedcredits+1, balance=balance-1 WHERE user_id=?",
            (user_id,)
        )

        conn.commit()
        query_id = cursor.lastrowid

    # =============================
    # RAG STORE
    # =============================
    await run_in_threadpool(store_query, query, text, "", language, llm_type)

    if video_id:
        background_tasks.add_task(process_video_background, video_id)

    return Response(
        text=text,
        video_id=video_id,
        llm_type=user_input.llm_type,
        query_id=query_id
    )

# =============================
# CREATE ORDER (GST)
# =============================
@app.post("/create-order")
def create_order(data: CreateOrder):

    cgst = data.amount * 0.09
    sgst = data.amount * 0.09
    total_amount = int(data.amount + cgst + sgst)

    order = razorpay_client.order.create({
        "amount": total_amount * 100,
        "currency": "INR"
    })

    return {
        "order_id": order["id"],
        "amount": total_amount,
        "cgst": cgst,
        "sgst": sgst,
        "credits": data.credits
    }

# =============================
# VERIFY PAYMENT (SECURE)
# =============================
@app.post("/verify-payment")
def verify_payment(data: VerifyPayment):

    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data.razorpay_order_id,
            "razorpay_payment_id": data.razorpay_payment_id,
            "razorpay_signature": data.razorpay_signature
        })
    except Exception:
        raise HTTPException(400, "Invalid payment signature")

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO payments
            (user_id,name,email,mobile_number,
             amount,cgst,sgst,total_amount,
             credits,razorpay_order_id,razorpay_payment_id,
             razorpay_signature,status)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                data.user_id,
                data.name,
                data.email,
                data.mobile_number,
                data.amount,
                data.cgst,
                data.sgst,
                data.total_amount,
                data.credits,
                data.razorpay_order_id,
                data.razorpay_payment_id,
                data.razorpay_signature,
                "success"
            )
        )

        conn.execute(
            "UPDATE credits SET totalcredits=totalcredits+?, balance=balance+? WHERE user_id=?",
            (data.credits, data.credits, data.user_id)
        )

        conn.commit()

    return {"status": "success"}

# =============================
# CREDIT HISTORY
# =============================
@app.get("/credit-history/{user_id}")
def credit_history(user_id: str):

    with get_db() as conn:
        row = conn.execute(
            "SELECT totalcredits,usedcredits,balance FROM credits WHERE user_id=?",
            (user_id,)
        ).fetchone()

    return dict(row) if row else {}

# =============================
# PAYMENT HISTORY
# =============================
@app.get("/payment-history/{user_id}")
def payment_history(user_id: str):

    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM payments WHERE user_id=? ORDER BY id DESC",
            (user_id,)
        ).fetchall()

    return [dict(r) for r in rows]

# =============================


#====================================voice api==================================================


# =============================
#  VOICE 
# =============================

@app.post("/voice", response_model=Response)
@limiter.limit("5/minute")
async def handle_voice(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = Form("en"),
    llm_type: str = Form("academic"),
    user_id: str = Form(None),    
    name: str = Form(None),
    email: str = Form(None),
    mobile_number: str = Form(None)
):

    # =============================
    # SAVE AUDIO FILE
    # =============================
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
    except Exception as e:
        return Response(text=f"File error: {str(e)}")

    try:
        # =============================
        # SPEECH → TEXT
        # =============================
        try:
            query = transcribe_audio_local(tmp_path)
        except Exception as e:
            return Response(
                text=f"Voice processing failed: {str(e)}",
                video_status="none",
                is_retrieved=False
            )

        if not query or not query.strip():
            return Response(
                text="Could not understand audio. Please try again.",
                video_status="none",
                is_retrieved=False
            )

        # =============================
        # LANGUAGE SAFE
        # =============================
        try:
            lang_enum = Language(language)
        except:
            lang_enum = Language.EN

        # =============================
        # USER ID DECODE
        # =============================
        try:
            decoded_user_id = base64.b64decode(user_id or "").decode()
        except:
            decoded_user_id = user_id or "guest"

        # =============================
        # CREATE USER QUERY OBJECT
        # =============================
        voice_user_input = UserQuery(
            user_id=decoded_user_id,
            name=name,
            email=email,
            mobile_number=mobile_number,
            query=query,
            language=lang_enum,
            llm_type=llm_type
        )

        # =============================
        # CALL MAIN ASK API
        # =============================
        return await ask_doubt(
            request,
            voice_user_input,
            background_tasks
        )

    finally:
        # =============================
        # CLEAN TEMP FILE
        # =============================
        try:
            os.unlink(tmp_path)
        except:
            pass

#====================================================================================================
# HEALTH
# =============================
@app.get("/health")
def health():
    return {"status": "running"}



# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)


# ========================================end new code==================================================