import chromadb

# Same path use karein jo aap rag.py me use karte hain
client = chromadb.PersistentClient(path="./chroma_db")

# Collection ka exact naam wahi hona chahiye jo rag.py me hai
collection = client.get_collection("ask_doubt_collection")

# Total count
print("Total records in Vector DB:", collection.count())

# Thoda data dekhne ke liye
results = collection.get(limit=5)

print("IDs:", results["ids"])
print("Documents:", results["documents"])
print("Metadatas:", results["metadatas"])
