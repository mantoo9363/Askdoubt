from pydantic import BaseModel
from typing import Optional
from enum import Enum


   # start  new code




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
# USER QUERY MODEL (UPDATED)
# =========================
class UserQuery(BaseModel):
    query: str
    input_type: InputType = InputType.TEXT
    
    # Language default 'HI' rakhein taaki Indian English accent aaye
    language: Language = Language.HI 

    # --- HEYGEN SETTINGS ---
    # Default Voice: Solemn Sachin (Hindi/Indian English)
    # Agar frontend se voice_id nahi aayi, to ye use hogi (No American Accent)
    voice_id: Optional[str] = None #"2fc30cb6995f458ca73ae87e3a74d644" 
    
    # Default Avatar: Joshua
    avatar_id: Optional[str] = None #"Joshua-incasual-20220826"

    # --- NEW FIELD FOR TEMPLATE VIDEO ---
    # Agar user ye URL bhejega, to 'Template Method' call hoga
    logo_url: Optional[str] = None  

    # Education metadata (OPTIONAL)
    class_name: Optional[str] = None
    subject_name: Optional[str] = None
    chapter_name: Optional[str] = None


# =========================
# API RESPONSE MODEL
# =========================
class Response(BaseModel):
    text: str

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


   #end new code
