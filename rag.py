


#=================================new code===========================================


#import os
#import uuid
#from typing import Optional, Tuple, List
#from dotenv import load_dotenv
#import chromadb
#import google.generativeai as genai

# =====================================================
# LOAD ENV
# =====================================================
#load_dotenv()

#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001")
#CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
#SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.85))

#if not GEMINI_API_KEY:
 #   raise RuntimeError("GEMINI_API_KEY missing in .env file")

# =====================================================
# CONFIGURE GEMINI
# =====================================================
#genai.configure(api_key=GEMINI_API_KEY)

# =====================================================
# CHROMA PERSISTENT CLIENT
# =====================================================
#chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

#collection = chroma_client.get_or_create_collection(
 #   name="ask_doubt"
#)

# =====================================================
# EMBEDDING FUNCTION
# =====================================================
#def embed_query(text: str) -> List[float]:
 #   """
  #  Generate Gemini embedding safely.
   # """
    #try:
     #   response = genai.embed_content(
      #      model=EMBED_MODEL,
       #     content=text
        #)
        #return response["embedding"]
    #except Exception:
     #   return []


# =====================================================
# STORE QUERY
# =====================================================
#def store_query(
 #   query: str,
  #  answer: str,
   # video_url: str = "",
    #language: str = "en"
#):
 #   query = query.strip().lower()
  #  embedding = embed_query(query)

   # if not embedding:
    #    return None

    #unique_id = str(uuid.uuid4())

    #collection.add(
     #   documents=[answer],
      #  embeddings=[embedding],
       # metadatas=[{
        #    "query": query,
         #   "video_url": video_url or "",
          #  "language": language
        #}],
        #ids=[unique_id]
    #)

    #return unique_id


# =====================================================
# RETRIEVE QUERY
# =====================================================
#def retrieve_query(
 #   query: str,
  #  language: str = "en"
#) -> Optional[Tuple[str, str]]:

 #   query = query.strip().lower()
  #  embedding = embed_query(query)

   # if not embedding:
    #    return None

    #results = collection.query(
     #   query_embeddings=[embedding],
      #  n_results=1,
       # where={"language": language}
    #)

    # Safety checks
    #if not results.get("documents"):
     #   return None

    #if len(results["documents"][0]) == 0:
     #   return None

    #if not results.get("distances"):
     #   return None

    #distance = results["distances"][0][0]
    #similarity = 1 - distance

    #if similarity >= SIMILARITY_THRESHOLD:
     #   answer = results["documents"][0][0]
      #  metadata = results["metadatas"][0][0]
       # return answer, metadata.get("video_url", "")

    #return None




#=================================end code============================================



#================================================rag new code ===========27 mar 2026=============

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

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.75))

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env file")

# =====================================================
# CONFIGURE GEMINI
# =====================================================
genai.configure(api_key=GEMINI_API_KEY)

# =====================================================
# CHROMA CLIENT
# =====================================================
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="ask_doubt"
)

# =====================================================
# EMBEDDING FUNCTION
# =====================================================
def embed_query(text: str) -> List[float]:
    try:
        response = genai.embed_content(
            model=EMBED_MODEL,
            content=text
        )
        return response["embedding"]
    except Exception as e:
        print("Embedding error:", str(e))
        return []

# =====================================================
# RETRIEVE QUERY (FINAL)
# =====================================================
def retrieve_query(
    query: str,
    language: str = "en",
    llm_type: str = "academic"
) -> Optional[Tuple[str, str]]:

    query = query.strip().lower()
    embedding = embed_query(query)

    if not embedding:
        return None

    try:
        results = collection.query(
            query_embeddings=[embedding],
            n_results=3,   #  Top-K
            where={
                "$and": [
                    {"language": {"$eq": language}},
                    {"llm_type": {"$eq": llm_type}}
                ]
            }
        )
    except Exception as e:
        print("Chroma query error:", str(e))
        return None

    if not results.get("documents") or len(results["documents"][0]) == 0:
        return None

    if not results.get("distances"):
        return None

    #  BEST MATCH
    best_idx = 0
    best_similarity = 0

    for i, dist in enumerate(results["distances"][0]):
        similarity = 1 - dist
        print(f"[RAG] Match {i} similarity:", similarity)

        if similarity > best_similarity:
            best_similarity = similarity
            best_idx = i

    if best_similarity >= SIMILARITY_THRESHOLD:
        answer = results["documents"][0][best_idx]
        metadata = results["metadatas"][0][best_idx]

        print("[RAG] Cache HIT ")

        return answer, metadata.get("video_url", "")

    print("[RAG] Cache MISS ")

    return None

# =====================================================
# STORE QUERY (FINAL)
# =====================================================
def store_query(
    query: str,
    answer: str,
    video_url: str = "",
    language: str = "en",
    llm_type: str = "academic"
):

    query = query.strip().lower()

    #  Duplicate check
    existing = retrieve_query(query, language, llm_type)
    if existing:
        print("[RAG] Duplicate detected, skipping store")
        return None

    embedding = embed_query(query)

    if not embedding:
        return None

    unique_id = str(uuid.uuid4())

    try:
        collection.add(
            documents=[answer],
            embeddings=[embedding],
            metadatas=[{
                "query": query,
                "video_url": video_url or "",
                "language": language,
                "llm_type": llm_type   #  IMPORTANT
            }],
            ids=[unique_id]
        )

        print("[RAG] Stored new query")

        return unique_id

    except Exception as e:
        print("Chroma store error:", str(e))
        return None





#=================================================end  new code ==================================
