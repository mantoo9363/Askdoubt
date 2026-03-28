import os
import whisper
import warnings

#  ADD THIS
os.environ["PATH"] += os.pathsep + "/usr/bin"

warnings.filterwarnings(
    "ignore",
    message="FP16 is not supported on CPU; using FP32 instead"
)

MODEL_SIZE = "tiny"
MODEL = whisper.load_model(MODEL_SIZE)

def transcribe_audio_local(audio_path: str, language: str = "en") -> str:

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    result = MODEL.transcribe(
        audio_path,
        language=language,
        fp16=False
    )

    text = result.get("text", "").strip()

    if not text:
        return "Sorry, I could not understand the audio."

    print("Transcription:", text)
    return text