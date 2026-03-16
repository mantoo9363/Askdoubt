
from pydantic import BaseModel
from typing import Optional
from enum import Enum


# =========================
# ENUMS
# =========================

class InputType(str, Enum):
    TEXT = "text"
    VOICE = "voice"


class Language(str, Enum):
    EN = "en"
    HI = "hi"


class VideoStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    NONE = "none"


# =========================
# USER QUERY MODEL
# =========================

class UserQuery(BaseModel):

    user_id: Optional[str] = None

    query: str
    input_type: InputType = InputType.TEXT

    # Default Hindi (Indian English accent)
    language: Language = Language.HI

    # HEYGEN SETTINGS
    voice_id: Optional[str] = None
    avatar_id: Optional[str] = None

    # Template logo
    logo_url: Optional[str] = None

    # Education metadata
    class_name: Optional[str] = None
    subject_name: Optional[str] = None
    chapter_name: Optional[str] = None


# =========================
# API RESPONSE MODEL
# =========================

class Response(BaseModel):

    text: str

    user_id: Optional[str] = None

    video_url: Optional[str] = None
    video_id: Optional[str] = None
    video_status: VideoStatus = VideoStatus.NONE

    transcript: Optional[str] = None

    class_name: Optional[str] = None
    subject_name: Optional[str] = None
    chapter_name: Optional[str] = None

    is_retrieved: bool = False
    query_id: Optional[int] = None

    download_url: Optional[str] = None


# =========================
# FEEDBACK MODEL
# =========================

class Feedback(BaseModel):

    query_id: int
    helpful: bool
    comment: Optional[str] = None


# =========================
# HEYGEN REQUEST MODEL
# =========================

class HeygenRequest(BaseModel):

    avatar_id: str
    voice_id: str
    script: str

    background: Optional[str] = "classroom"
    aspect_ratio: Optional[str] = "16:9"
    language: Language = Language.EN


# =========================
# RAZORPAY PAYMENT MODELS
# =========================

class CreateOrder(BaseModel):

    user_id: str
    amount: int
    credits: int


class VerifyPayment(BaseModel):

    user_id: str
    amount: int
    credits: int

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
