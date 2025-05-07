from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    try:
        return FAISS.load_local(settings.RAG_DB_PATH, embeddings)
    except:
        return FAISS.from_texts(["No documents loaded"], embedding=embeddings)