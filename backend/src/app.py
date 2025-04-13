from flask import Config, Flask, g, current_app
from src.configs.config import DevConfig, QdrantConfig, GradioConfig, GoogleConfig, LangsmithConfig, MongoConfig, OllamaConfig, GroqConfig, HuggingFaceConfig
from src.utils.rag_pipeline import RagPipeline
from src.utils.chatbot import Chatbot, OutputParserTypes
from flask_pymongo import PyMongo
from src.utils.vector_db import VectorDb
import os


def get_db():
    config = current_app.config
    if 'db' not in g:
        try:
            mongo_uri = f"mongodb://{config.get('MONGO_HOST')}:{config.get('MONGO_PORT')}/{config.get('MONGO_DBNAME')}"
            db = PyMongo(current_app, uri=mongo_uri).db
            g.db = db
        except Exception as e:
            current_app.logger.error(f"Error connecting to database: {e}")
            raise
    return g.db

def get_qdrant() -> VectorDb:
    config = current_app.config
    if 'qdrant' not in g:
        try:
            qdrant = VectorDb(
                url=config.get('QDRANT_URL'),
                api_key=config.get('QDRANT_API_KEY')
            )
            qdrant.set_embedding_model()
            g.qdrant = qdrant
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Qdrant: {e}")
            raise      
    return g.qdrant
    
def get_chat():
    if 'chat' not in g:
        chat = Chatbot()
        chat.set_parser(OutputParserTypes.STRING)
        qdrant = get_qdrant()
        chat.set_vector_store(qdrant.get_collection("products"))
        g.chat = chat
    return g.chat
    
def get_rag_pipeline():
    if '_rag_pipeline' not in g:
        chat = get_chat()
        qdrant = get_qdrant()
        rag_pipeline = RagPipeline(
            chat.vector_store,
            search_k=3,
            model=chat.model,
            embedding_model=qdrant.embeddings
        )
        rag_pipeline.set_history_aware_retriever()
        rag_pipeline.set_qa_chain()
        rag_pipeline.set_rag_chain()
        g.rag_pipeline = rag_pipeline
    return g.rag_pipeline

def create_app():
    app = Flask(__name__)
        
    # set app configurations
    # env = dotenv_values(".env")
    app.config.from_object(DevConfig)
    app.config.from_object(GoogleConfig)
    app.config.from_object(QdrantConfig)
    app.config.from_object(GradioConfig)
    app.config.from_object(LangsmithConfig)
    app.config.from_object(MongoConfig)
    app.config.from_object(OllamaConfig)
    app.config.from_object(GroqConfig)
    app.config.from_object(HuggingFaceConfig)

    with app.app_context():
        try:
            mongo_uri = f"mongodb://{app.config.get('MONGO_HOST')}:{app.config.get('MONGO_PORT')}/{app.config.get('MONGO_DBNAME')}"
            print(f"mongo url: {mongo_uri}")
            mongo = PyMongo(app, uri=mongo_uri)
            app.config['MONGO'] = mongo
            g.db = mongo.db
        except Exception as e:
            app.logger.error(f"Error connecting to database: {e}")
            raise
        
        try:
            get_qdrant()
        except Exception as e:
            app.logger.error(f"Failed to initialize Qdrant: {e}")
            raise
        
        app.config['QDRANT'] = get_qdrant
        app.config['CHAT'] = get_chat
        app.config['RAG_PIPELINE'] = get_rag_pipeline
        
        @app.teardown_appcontext
        def teardown_db(exception):
            db = g.pop('db', None)
            if db is not None:
                # Perform any necessary teardown for database if needed
                pass

        @app.teardown_appcontext
        def teardown_qdrant(exception):
            qdrant = g.pop('qdrant', None)
            if qdrant is not None:
                # Perform any necessary teardown for qdrant if needed
                pass
    
        @app.teardown_appcontext
        def teardown_gemini_chat(exception):
            chat = g.pop('chat', None)
            if chat is not None:
                # Perform any necessary teardown for chat if needed
                pass
     
    with app.app_context():   
        from src.routes import api_bp
        app.register_blueprint(api_bp, url_prefix="/api")
        
    return app