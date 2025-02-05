from dotenv import dotenv_values
env = dotenv_values("../.env")

class Config:
    """Base config."""

class DevConfig(Config):
    FLASK_ENV = env.get('FLASK_ENV')
    DEBUG = True
    TESTING = True
    DATABASE_URL = env.get('DATABASE_URL')
    GRADIO_URL = env.get('GRADIO_URL')
    NGROK_AUTH_TOKEN = env.get('NGROK_AUTH_TOKEN')
    NGROK_STATIC_DOMAIN = env.get('NGROK_STATIC_DOMAIN')
    NGROK_API_KEY = env.get('NGROK_API_KEY')

class QdrantConfig(Config):
    QDRANT_URL = env.get('QDRANT_CLUSTER_URL')
    QDRANT_API_KEY = env.get('QDRANT_API_KEY')

class GradioConfig(Config):
    GRADIO_URL = env.get('GRADIO_URL')
    GRADIO_PORT = env.get('GRADIO_PORT')

class GoogleConfig(Config):
    GOOGLE_GENERATIVE_LANGUAGE_API_KEY= env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
    
class LangsmithConfig(Config):
    LANGCHAIN_TRACING_V2 = env.get('LANGCHAIN_TRACING_V2')
    LANGCHAIN_ENDPOINT = env.get('LANGCHAIN_ENDPOINT')
    LANGCHAIN_API_KEY = env.get('LANGCHAIN_API_KEY')
    LANGCHAIN_PROJECT = env.get('LANGCHAIN_PROJECT')