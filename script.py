import os
import whisper
import warnings

warnings.filterwarnings(
    "ignore",
    message="FP16 is not supported on CPU; using FP32 instead"
)

# -------------------------------
# Load Whisper model ONCE
# -------------------------------
# tiny / base / small (tiny is fastest)
MODEL_SIZE = "tiny"
MODEL = whisper.load_model(MODEL_SIZE)

# -------------------------------
# Transcribe local audio (.wav)
# -------------------------------
def transcribe_audio_local(
    audio_path: str,
    language: str = "en"
) -> str:
    """
    audio_path: path to wav file
    language: "en" or "hi"
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    result = MODEL.transcribe(
        audio_path,
        language=language,
        fp16=False   # IMPORTANT for Windows CPU
    )

    text = result.get("text", "").strip()

    if not text:
        return "Sorry, I could not understand the audio."

    print(" Transcription:", text)
    return text
