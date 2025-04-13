from langchain_ollama.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from src.configs.config import OllamaConfig, GoogleConfig
from flask import current_app as app

class RagHelper:
    def __init__(self) -> None:
        self.model = None
        self.embeddings = None
        
        if app.config.get('USE_OLLAMA'):
            self.model = ChatOllama(
                base_url = app.config.get('OLLAMA_URL'),
                model = app.config.get('OLLAMA_MODEL_ID'),
                temperature = 0.5
            )
        elif app.config.get('USE_GEMINI'):
            self.model = ChatGoogleGenerativeAI(
                model= app.config.get('GEMINI_MODEL_ID'), 
                google_api_key= app.config.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'),
                temperature=0.5,
                convert_system_message_to_human=True
            )
        elif app.config.get('USE_GROQ'):
            self.model = ChatGroq(
                model= app.config.get('GROQ_MODEL_ID'),
                api_key= app.config.get('GROQ_API_KEY'),
                temperature=0.5,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            
        if app.config.get('USE_OLLAMA_EMBEDDING'):
            print(f"using ollama embedding: {app.config.get('OLLAMA_EMBEDDING_MODEL_ID')}")
            self.embeddings = OllamaEmbeddings(
                base_url= app.config.get('OLLAMA_URL'), 
                model= app.config.get('OLLAMA_EMBEDDING_MODEL_ID')
            )
        elif app.config.get('USE_GOOGLE_EMBEDDING'):
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model= app.config.get('GEMINI_EMBEDDING_MODEL_ID'), 
                google_api_key= app.config.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
            )
        elif app.config.get('USE_HUGGINGFACE_EMBEDDING'):
            self.embeddings = HuggingFaceBgeEmbeddings(
                model_name= app.config.get('HUGGINGFACE_EMBEDDING_MODEL_ID'), 
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
            
    def get_llm(self):
        return self.model
    
    def get_embedding_model(self):
        return self.embeddings
        