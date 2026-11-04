from functools import lru_cache
import chromadb
from chromadb.utils import embedding_functions
from app.config import EMBEDDING_MODEL_NAME

@lru_cache(maxsize=1)
def get_collection():
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
    return chromadb.EphemeralClient().get_or_create_collection(name="knowledge_base", embedding_function=embedding_fn)

def load_knowledge_base(chunks: list[str]):
    collection = get_collection()
    existing = collection.get()["ids"]
    if existing:
        collection.delete(ids=existing)
    if chunks:
        collection.add(documents=chunks, ids=[f"chunk_{i}" for i in range(len(chunks))])

def retrieve(question: str, top_k: int = 2):
    collection = get_collection()
    count = collection.count()
    if not count:
        return "", []
    results = collection.query(query_texts=[question], n_results=min(top_k, count))
    sources = results["documents"][0]
    return "\n".join(sources), sources
