from dotenv import dotenv_values
from flask import Flask, g
from configs.database import Database
from configs.config import DevConfig, QdrantConfig, GradioConfig, GoogleConfig
from utils.chatbot import Chatbot, OutputParserTypes
from utils.database import create_all, is_database_created
from utils.vector_db import VectorDb

def create_app():
    app = Flask(__name__)

    env = dotenv_values("../.env")
    app.config.from_object(DevConfig)
    app.config.from_object(GoogleConfig)
    app.config.from_object(QdrantConfig)
    app.config.from_object(GradioConfig)

    db = Database(app.config.get('DATABASE_URL'))
    db.connect()

    def get_db() -> Database:
        if 'db' not in g:
            g.db = db
        return g.db

    if is_database_created(db) == False:
        create_all(db)

    qdrant = VectorDb(
        env.get('QDRANT_CLUSTER_URL'), 
        env.get('QDRANT_API_KEY')
    )
    qdrant.set_embedding_model(model_id="llama3.1")

    def get_qdrant() -> VectorDb:
        if 'qdrant' not in g:
            g.qdrant = qdrant
        return g.qdrant
    
    def get_gemini_chat():
        if 'chat' not in g:
            gemini_chat = Chatbot(model_id="llama3.1")
            gemini_chat.set_parser(OutputParserTypes.STRING)
            gemini_chat.set_vector_store(app.config['QDRANT']().get_collection("products"))
            g.chat = gemini_chat
        return g.chat

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

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
            # Perform any necessary teardown for qdrant if needed
            pass
    
    from routes import api_bp
    
    app.config['DB'] = get_db
    app.config['QDRANT'] = get_qdrant
    app.config['CHAT'] = get_gemini_chat

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix="/api")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)