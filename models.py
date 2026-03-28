
#from pydantic import BaseModel
#from typing import Optional
#from enum import Enum


# =========================
# ENUMS
# =========================

#class InputType(str, Enum):
 #   TEXT = "text"
  #  VOICE = "voice"


#class Language(str, Enum):
 #   EN = "en"
  #  HI = "hi"


#class VideoStatus(str, Enum):
 #   PROCESSING = "processing"
  #  COMPLETED = "completed"
   # NONE = "none"


# =========================
# USER QUERY MODEL
# =========================

#class UserQuery(BaseModel):

 #   user_id: Optional[str] = None

  #  query: str
   # input_type: InputType = InputType.TEXT

    # Default Hindi (Indian English accent)
   # language: Language = Language.HI

    # HEYGEN SETTINGS
   # voice_id: Optional[str] = None
    #avatar_id: Optional[str] = None

    # Template logo
    #logo_url: Optional[str] = None

    # Education metadata
   # class_name: Optional[str] = None
    #subject_name: Optional[str] = None
    #chapter_name: Optional[str] = None


# =========================
# API RESPONSE MODEL
# =========================

#class Response(BaseModel):

 #   text: str

  #  user_id: Optional[str] = None

   # video_url: Optional[str] = None
   # video_id: Optional[str] = None
   # video_status: VideoStatus = VideoStatus.NONE

   # transcript: Optional[str] = None

   # class_name: Optional[str] = None
   # subject_name: Optional[str] = None
   # chapter_name: Optional[str] = None

   # is_retrieved: bool = False
   # query_id: Optional[int] = None

   # download_url: Optional[str] = None


# =========================
# FEEDBACK MODEL
# =========================

#class Feedback(BaseModel):

 #   query_id: int
  #  helpful: bool
   # comment: Optional[str] = None


# =========================
# HEYGEN REQUEST MODEL
# =========================

#class HeygenRequest(BaseModel):

 #   avatar_id: str
  #  voice_id: str
   # script: str

    #background: Optional[str] = "classroom"
    #aspect_ratio: Optional[str] = "16:9"
    #language: Language = Language.EN


# =========================
# RAZORPAY PAYMENT MODELS
# =========================

#class CreateOrder(BaseModel):

 #   user_id: str
  #  amount: int
   # credits: int


#class VerifyPayment(BaseModel):

 #   user_id: str
  #  amount: int
   # credits: int

   # razorpay_order_id: str
   # razorpay_payment_id: str
   # razorpay_signature: str


#=============================new modals----------------------------------------
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime


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


#  FINAL LLM TYPE (MODE + LANGUAGE)
class LLMType(str, Enum):
    # MAIN MODES
    ACADEMIC = "academic"
    SKILL = "skill"
    ENTREPRENEURSHIP = "entrepreneurship"
    COMPETITIVE = "competitive"

    #  LANGUAGE LEARNING
    IELTS = "ielts"
    FRENCH = "french"
    ARABIC = "arabic"
    SANSKRIT = "sanskrit"
    GERMAN = "german"
    SPANISH = "spanish"


# =========================
# USER QUERY MODEL
# =========================

class UserQuery(BaseModel):

    user_id: Optional[str] = None

    # USER DETAILS
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None

    query: str
    input_type: InputType = InputType.TEXT

    #  SINGLE FIELD FOR ALL TYPES
    llm_type: LLMType = LLMType.ACADEMIC

    # Default Hindi
    language: Language = Language.HI

    # HEYGEN SETTINGS
    voice_id: Optional[str] = None
    avatar_id: Optional[str] = None

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

    llm_type: Optional[LLMType] = None

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

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None

    # Base amount (without GST)
    amount: int

    # GST BREAKUP
    cgst: Optional[float] = 0.0
    sgst: Optional[float] = 0.0

    # FINAL AMOUNT
    total_amount: int

    credits: int


class VerifyPayment(BaseModel):

    user_id: str

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None

    amount: int

    cgst: Optional[float] = 0.0
    sgst: Optional[float] = 0.0
    total_amount: int

    credits: int

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


# =========================
# PAYMENT DB MODEL
# =========================

class Payment(BaseModel):

    payment_id: Optional[int] = None

    user_id: str

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None

    amount: int
    cgst: float = 0.0
    sgst: float = 0.0
    total_amount: int

    credits: int

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

    status: str = "success"

    created_at: Optional[datetime] = datetime.utcnow()


# =========================
# CREDIT TABLE MODEL
# =========================

class Credit(BaseModel):

    credit_id: Optional[int] = None

    user_id: str

    total_credits: int = 0
    used_credits: int = 0
    balance_credits: int = 0

    updated_at: Optional[datetime] = datetime.utcnow()


# =========================
# CREDIT TRANSACTION
# =========================

class CreditTransaction(BaseModel):

    transaction_id: Optional[int] = None

    user_id: str

    credits_added: int = 0
    credits_used: int = 0

    transaction_type: str  # "credit" / "debit"

    reference: Optional[str] = None

    created_at: Optional[datetime] = datetime.utcnow()

# end new modals-------date=======27-mar-2026===========================================
