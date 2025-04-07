from dotenv import dotenv_values
import os

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
env = dotenv_values(env_path)

class Config:
    """Base config."""
    
class DevConfig(Config):
    FLASK_ENV = env.get('FLASK_ENV') or os.environ.get('FLASK_ENV')
    DEBUG = True
    TESTING = True
    DATABASE_URL = env.get('DATABASE_URL') or os.environ.get('DATABASE_URL')
    NGROK_AUTH_TOKEN = env.get('NGROK_AUTH_TOKEN') or os.environ.get('NGROK_AUTH_TOKEN')
    NGROK_STATIC_DOMAIN = env.get('NGROK_STATIC_DOMAIN') or os.environ.get('NGROK_STATIC_DOMAIN')
    NGROK_API_KEY = env.get('NGROK_API_KEY') or os.environ.get('NGROK_API_KEY')
    USE_GROQ = env.get('USE_GROQ') or os.environ.get('USE_GROQ')
    USE_OLLAMA = env.get('USE_OLLAMA') or os.environ.get('USE_OLLAMA')
    USE_GEMINI = env.get('USE_GEMINI') or os.environ.get('USE_GEMINI')
    USE_HUGGINGFACE_EMBEDDING = env.get('USE_HUGGINGFACE_EMBEDDING') or os.environ.get('USE_HUGGINGFACE_EMBEDDING')
    USE_GOOGLE_EMBEDDING = env.get('USE_GOOGLE_EMBEDDING') or os.environ.get('USE_GOOGLE_EMBEDDING')
    USE_OLLAMA_EMBEDDING = env.get('USE_OLLAMA_EMBEDDING') or os.environ.get('USE_OLLAMA_EMBEDDING')
    
class MongoConfig(Config):
    MONGO_HOST = env.get('MONGO_HOST') or os.environ.get('MONGO_HOST')
    MONGO_PORT = env.get('MONGO_PORT') or os.environ.get('MONGO_PORT')
    MONGO_USERNAME = env.get('MONGO_USERNAME') or os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = env.get('MONGO_PASSWORD') or os.environ.get('MONGO_PASSWORD')
    MONGO_DBNAME = env.get('MONGO_DBNAME') or  os.environ.get('MONGO_DBNAME')

class QdrantConfig(Config):
    QDRANT_URL = env.get('QDRANT_CLUSTER_URL') or  os.environ.get('QDRANT_CLUSTER_URL')
    QDRANT_API_KEY = env.get('QDRANT_API_KEY') or os.environ.get('QDRANT_API_KEY')

class GradioConfig(Config):
    GRADIO_URL = env.get('GRADIO_URL') or os.environ.get('GRADIO_URL')
    GRADIO_PORT = env.get('GRADIO_PORT') or os.environ.get('GRADIO_PORT')

class OllamaConfig(Config):
    OLLAMA_URL = env.get('OLLAMA_URL') or os.environ.get('OLLAMA_URL')
    OLLAMA_MODEL_ID = env.get('OLLAMA_MODEL_ID') or os.environ.get('OLLAMA_MODEL_ID')
    OLLAMA_EMBEDDING_MODEL_ID = env.get('OLLAMA_EMBEDDING_MODEL_ID') or os.environ.get('OLLAMA_EMBEDDING_MODEL_ID')

class GoogleConfig(Config):
    GOOGLE_GENERATIVE_LANGUAGE_API_KEY = env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY') or os.environ.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
    GEMINI_MODEL_ID = env.get('GEMINI_MODEL_ID') or os.environ.get('GEMINI_MODEL_ID')
    GEMINI_EMBEDDING_MODEL_ID = env.get('GEMINI_EMBEDDING_MODEL_ID') or os.environ.get('GEMINI_EMBEDDING_MODEL_ID')

class GroqConfig(Config):
    GROQ_API_KEY = env.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
    GROQ_MODEL_ID = env.get('GROQ_MODEL_ID') or os.environ.get('GROQ_MODEL_ID')

class HuggingFaceConfig(Config):
    HUGGINGFACE_EMBEDDING_MODEL_ID = env.get('HUGGINGFACE_EMBEDDING_MODEL_ID') or os.environ.get('HUGGINGFACE_EMBEDDING_MODEL_ID')
    
class LangsmithConfig(Config):
    LANGSMITH_TRACING = env.get('LANGSMITH_TRACING') or os.environ.get('LANGSMITH_TRACING')
    LANGSMITH_ENDPOINT = env.get('LANGSMITH_ENDPOINT') or os.environ.get('LANGSMITH_ENDPOINT')
    LANGSMITH_API_KEY = env.get('LANGSMITH_API_KEY') or os.environ.get('LANGSMITH_API_KEY')
    LANGSMITH_PROJECT = env.get('LANGSMITH_PROJECT') or os.environ.get('LANGSMITH_PROJECT')