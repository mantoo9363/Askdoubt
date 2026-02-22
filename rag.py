


#=================================new code===========================================


import os
import uuid
from typing import Optional, Tuple, List
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai

# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.85))

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env file")

# =====================================================
# CONFIGURE GEMINI
# =====================================================
genai.configure(api_key=GEMINI_API_KEY)

# =====================================================
# CHROMA PERSISTENT CLIENT
# =====================================================
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="ask_doubt"
)

# =====================================================
# EMBEDDING FUNCTION
# =====================================================
def embed_query(text: str) -> List[float]:
    """
    Generate Gemini embedding safely.
    """
    try:
        response = genai.embed_content(
            model=EMBED_MODEL,
            content=text
        )
        return response["embedding"]
    except Exception:
        return []


# =====================================================
# STORE QUERY
# =====================================================
def store_query(
    query: str,
    answer: str,
    video_url: str = "",
    language: str = "en"
):
    query = query.strip().lower()
    embedding = embed_query(query)

    if not embedding:
        return None

    unique_id = str(uuid.uuid4())

    collection.add(
        documents=[answer],
        embeddings=[embedding],
        metadatas=[{
            "query": query,
            "video_url": video_url or "",
            "language": language
        }],
        ids=[unique_id]
    )

    return unique_id


# =====================================================
# RETRIEVE QUERY
# =====================================================
def retrieve_query(
    query: str,
    language: str = "en"
) -> Optional[Tuple[str, str]]:

    query = query.strip().lower()
    embedding = embed_query(query)

    if not embedding:
        return None

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
        where={"language": language}
    )

    # Safety checks
    if not results.get("documents"):
        return None

    if len(results["documents"][0]) == 0:
        return None

    if not results.get("distances"):
        return None

    distance = results["distances"][0][0]
    similarity = 1 - distance

    if similarity >= SIMILARITY_THRESHOLD:
        answer = results["documents"][0][0]
        metadata = results["metadatas"][0][0]
        return answer, metadata.get("video_url", "")

    return None




#=================================end code============================================
