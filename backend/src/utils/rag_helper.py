from dotenv import dotenv_values
from langchain_ollama.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.embeddings import OllamaEmbeddings
from langchain.embeddings import HuggingFaceBgeEmbeddings

env = dotenv_values("../.env")

class RagHelper:
    def __init__(self) -> None:
        self.model = None
        self.embeddings = None
        
        if eval(env.get('USE_OLLAMA')) == True:
            print("using ollama model...")
            self.model = ChatOllama(
                base_url=env.get('OLLAMA_URL'),
                model=env.get('OLLAMA_MODEL_ID'),
                temperature=0.5
            )
        elif eval(env.get('USE_GEMINI')) == True:
            self.model = ChatGoogleGenerativeAI(
                model=env.get('GEMINI_MODEL_ID'), 
                google_api_key=env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'),
                temperature=0.5,
                convert_system_message_to_human=True
            )
        elif eval(env.get('USE_GROQ')) == True:
            self.model = ChatGroq(
                model=env.get('GROQ_MODEL_ID'),
                api_key=env.get('GROQ_API_KEY'),
                temperature=0.5,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            
        if eval(env.get('USE_OLLAMA_EMBEDDING')) == True:
            print("using ollama embeddings...")
            self.embeddings = OllamaEmbeddings(
                base_url= env.get('OLLAMA_URL'), 
                model=env.get('OLLAMA_EMBEDDING_MODEL_ID')
            )
        elif eval(env.get('USE_GOOGLE_EMBEDDING')) == True:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=env.get('GEMINI_EMBEDDING_MODEL_ID'), 
                google_api_key=env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
            )
        elif eval(env.get('USE_HUGGINGFACE_EMBEDDING')) == True:
            self.embeddings = HuggingFaceBgeEmbeddings(
                model_name=env.get('HUGGINGFACE_EMBEDDING_MODEL_ID'), 
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
            
    def get_llm(self):
        return self.model
    
    def get_embedding_model(self):
        return self.embeddings
        