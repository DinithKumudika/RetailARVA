import gradio as gr
from dotenv import dotenv_values
from gradio import ChatMessage
from utils.vector_db import VectorDb
from utils.chatbot import Chatbot, OutputParserTypes
from langchain_core.messages import HumanMessage, AIMessage
from configs.database import Database
import os

env = dotenv_values("../.env")

os.environ["LANGCHAIN_TRACING_V2"] = env.get('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_ENDPOINT"] = env.get('LANGCHAIN_ENDPOINT')
os.environ["LANGCHAIN_API_KEY"] = env.get('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_PROJECT"] = env.get('LANGCHAIN_PROJECT')


def qdrant_init():
    qdrant = VectorDb(
        env.get('QDRANT_CLUSTER_URL'), 
        env.get('QDRANT_API_KEY')
    )
    qdrant.set_embedding_model()
    print("embeddings: ", qdrant.embeddings)
    return qdrant

def db_init():
    db = Database(env.get('DATABASE_URL'))
    db.connect()
    return db

def chat_init():
    db = db_init()
    gemini_chat = Chatbot(db)
    gemini_chat.set_parser(OutputParserTypes.STRING)
    
    qdrant = qdrant_init()
    gemini_chat.set_vector_store(qdrant.get_collection("products"))
    return gemini_chat

gemini_chat = chat_init()

def greet_user():
    greeting = gemini_chat.greet()
    return greeting


def chat_fucntion(message, history: list):
    chat_response = gemini_chat.invoke(message)

    return chat_response

gr.ChatInterface(
    fn=chat_fucntion,
    title="RetailARVA Bot",
    chatbot=gr.Chatbot(height=500, value=[[None, greet_user()]]),
    textbox=gr.Textbox(placeholder="Message chatbot", container=False, scale=7),
    theme=gr.themes.Monochrome(),
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear"
).launch(share=True, debug=True)