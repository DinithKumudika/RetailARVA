from dotenv import dotenv_values
env = dotenv_values("../.env")

class Config:
    """Base config."""

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URL = env.get('DATABASE_URL')
    GRADIO_URL = env.get('GRADIO_URL')

class QdrantConfig(Config):
    QDRANT_URL = env.get('QDRANT_CLUSTER_URL')
    QDRANT_API_KEY = env.get('QDRANT_API_KEY')

class GradioConfig(Config):
    GRADIO_URL = env.get('GRADIO_URL')
    GRADIO_PORT = env.get('GRADIO_PORT')

class GoogleConfig(Config):
    GOOGLE_GENERATIVE_LANGUAGE_API_KEY= env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')