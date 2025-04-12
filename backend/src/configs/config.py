from dotenv import dotenv_values
import os

# env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
# env = dotenv_values(env_path)

class Config:
    """Base config."""
    
class DevConfig(Config):
    FLASK_ENV = os.environ.get('FLASK_ENV')
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.environ.get('DATABASE_URL')
    NGROK_AUTH_TOKEN = os.environ.get('NGROK_AUTH_TOKEN')
    NGROK_STATIC_DOMAIN = os.environ.get('NGROK_STATIC_DOMAIN')
    NGROK_API_KEY = os.environ.get('NGROK_API_KEY')
    USE_GROQ = os.environ.get('USE_GROQ')
    USE_OLLAMA = os.environ.get('USE_OLLAMA')
    USE_GEMINI = os.environ.get('USE_GEMINI')
    USE_HUGGINGFACE_EMBEDDING = os.environ.get('USE_HUGGINGFACE_EMBEDDING')
    USE_GOOGLE_EMBEDDING = os.environ.get('USE_GOOGLE_EMBEDDING')
    USE_OLLAMA_EMBEDDING = os.environ.get('USE_OLLAMA_EMBEDDING')
    
class MongoConfig(Config):
    MONGO_HOST = os.environ.get('MONGO_HOST')
    MONGO_PORT = os.environ.get('MONGO_PORT')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')

class QdrantConfig(Config):
    QDRANT_URL = os.environ.get('QDRANT_CLUSTER_URL')
    QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')

class GradioConfig(Config):
    GRADIO_URL = os.environ.get('GRADIO_URL')
    GRADIO_PORT = os.environ.get('GRADIO_PORT')

class OllamaConfig(Config):
    OLLAMA_URL = os.environ.get('OLLAMA_URL')
    OLLAMA_MODEL_ID = os.environ.get('OLLAMA_MODEL_ID')
    OLLAMA_EMBEDDING_MODEL_ID = os.environ.get('OLLAMA_EMBEDDING_MODEL_ID')

class GoogleConfig(Config):
    GOOGLE_GENERATIVE_LANGUAGE_API_KEY = os.environ.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
    GEMINI_MODEL_ID = os.environ.get('GEMINI_MODEL_ID')
    GEMINI_EMBEDDING_MODEL_ID = os.environ.get('GEMINI_EMBEDDING_MODEL_ID')

class GroqConfig(Config):
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GROQ_MODEL_ID = os.environ.get('GROQ_MODEL_ID')

class HuggingFaceConfig(Config):
    HUGGINGFACE_EMBEDDING_MODEL_ID = os.environ.get('HUGGINGFACE_EMBEDDING_MODEL_ID')
    
class LangsmithConfig(Config):
    LANGSMITH_TRACING = os.environ.get('LANGSMITH_TRACING')
    LANGSMITH_ENDPOINT = os.environ.get('LANGSMITH_ENDPOINT')
    LANGSMITH_API_KEY = os.environ.get('LANGSMITH_API_KEY')
    LANGSMITH_PROJECT = os.environ.get('LANGSMITH_PROJECT')