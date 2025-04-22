from sentence_transformers import CrossEncoder
from langchain_qdrant import QdrantVectorStore
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from src.utils.rag_helper import RagHelper

# TODO: Remove RAG pipeline

class RagPipeline:
     def __init__(self, vector_store: QdrantVectorStore, search_k: int):
          pass
     
     def invoke(self, query: str, chat_history: list):
          pass
