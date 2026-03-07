from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="rag/vector_db",
    embedding_function=embeddings
)

def retrieve_context(query, k=3):
    results = db.similarity_search(query, k=k)
    return results