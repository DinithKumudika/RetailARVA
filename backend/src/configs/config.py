from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    """Base config."""
    
class DevConfig(Config):
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    TESTING = os.getenv('TESTING', 'True').lower() == 'true'
    DATABASE_URL = os.getenv('DATABASE_URL')

    # Ngrok configurations
    NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')
    NGROK_STATIC_DOMAIN = os.getenv('NGROK_STATIC_DOMAIN')
    NGROK_API_KEY = os.getenv('NGROK_API_KEY')

    # Model usage flags
    USE_GROQ = os.getenv('USE_GROQ', 'False').lower() == 'true'
    USE_OLLAMA = os.getenv('USE_OLLAMA', 'False').lower() == 'true'
    USE_GEMINI = os.getenv('USE_GEMINI', 'False').lower() == 'true'
    USE_HUGGINGFACE_EMBEDDING = os.getenv('USE_HUGGINGFACE_EMBEDDING', 'False').lower() == 'true'
    USE_GOOGLE_EMBEDDING = os.getenv('USE_GOOGLE_EMBEDDING', 'False').lower() == 'true'
    USE_OLLAMA_EMBEDDING = os.getenv('USE_OLLAMA_EMBEDDING', 'False').lower() == 'true'

class MongoConfig(Config):
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = os.getenv('MONGO_PORT')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')

class QdrantConfig(Config):
    QDRANT_URL = os.getenv('QDRANT_CLUSTER_URL')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

class GradioConfig(Config):
    GRADIO_URL = os.getenv('GRADIO_URL', 'http://127.0.0.1:7860')
    GRADIO_PORT = os.getenv('GRADIO_PORT', '7860')

class OllamaConfig(Config):
    OLLAMA_URL = os.getenv('OLLAMA_URL')
    OLLAMA_MODEL_ID = os.getenv('OLLAMA_MODEL_ID')
    OLLAMA_EMBEDDING_MODEL_ID = os.getenv('OLLAMA_EMBEDDING_MODEL_ID')

class GoogleConfig(Config):
    GOOGLE_GENERATIVE_LANGUAGE_API_KEY = os.getenv('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
    GEMINI_MODEL_ID = os.getenv('GEMINI_MODEL_ID')
    GEMINI_EMBEDDING_MODEL_ID = os.getenv('GEMINI_EMBEDDING_MODEL_ID')

class GroqConfig(Config):
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL_ID = os.getenv('GROQ_MODEL_ID', 'llama-3.1-8b-instant')

class HuggingFaceConfig(Config):
    HUGGINGFACE_EMBEDDING_MODEL_ID = os.getenv('HUGGINGFACE_EMBEDDING_MODEL_ID', 'BAAI/bge-large-en-v1.5')
    
class LangsmithConfig(Config):
    LANGSMITH_TRACING = os.getenv('LANGSMITH_TRACING', 'False').lower() == 'true'
    LANGSMITH_ENDPOINT = os.getenv('LANGSMITH_ENDPOINT', 'https://api.smith.langchain.com')
    LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY')
    LANGSMITH_PROJECT = os.getenv('LANGSMITH_PROJECT', 'retailarva-chatbot')