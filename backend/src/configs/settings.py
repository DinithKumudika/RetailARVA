import os
from dotenv import dotenv_values
from pydantic_settings import BaseSettings

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'development':
    env = dotenv_values("../.env")
else:
    env = {}

class AppSettings(BaseSettings):
    ENVIRONMENT: str = env.get('ENVIRONMENT') or os.getenv('ENVIRONMENT', 'development')

    class Config:
        case_sensitive = True

class GoogleSettings(BaseSettings):
    GOOGLE_GENERATIVE_LANGUAGE_API_KEY : str = env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY') or os.getenv('GOOGLE_GENERATIVE_LANGUAGE_API_KEY', None)
    GOOGLE_APPLICATION_CREDENTIALS : str = env.get('GOOGLE_APPLICATION_CREDENTIALS') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)

    class Config:
        case_sensitive = True


class Settings(AppSettings, GoogleSettings):
    pass

try:
    settings = Settings()
except ValueError as e:
    print(f"Error initializing settings: {e}")
    raise
