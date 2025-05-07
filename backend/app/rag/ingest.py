from langchain_text_splitters import RecursiveCharacterTextSplitter
from .retriever import get_retriever
from app.core.config import settings

def ingest_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    splits = text_splitter.split_documents(docs)
    
    vectorstore = get_retriever()
    vectorstore.add_documents(splits)
    vectorstore.save_local(settings.RAG_DB_PATH)