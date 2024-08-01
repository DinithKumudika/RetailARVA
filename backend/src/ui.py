import random
import gradio as gr
from utils.gemini_chat import GeminiChat, OutputParserTypes
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import dotenv_values

from utils.vector_db import VectorDb

env = dotenv_values("../.env")

qdrant = VectorDb(
    env.get('QDRANT_CLUSTER_URL'), 
    env.get('QDRANT_API_KEY')
)
qdrant.set_embedding_model(model_id="models/embedding-001", api_key=env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'))

def chat_fucntion(message, history):
    gemini_chat = GeminiChat(env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'))
    gemini_chat.set_parser(OutputParserTypes.STRING)
    gemini_chat.set_vector_store(qdrant.get_collection("products"))
    chat_response = gemini_chat.invoke(message)

    gemini_chat.chatHistory.extend([
        HumanMessage(content=message),
        AIMessage(content=chat_response.content)
    ])

    return chat_response.content

gr.ChatInterface(
    chat_fucntion,
    title="RetailARVA Bot",
    chatbot=gr.Chatbot(height=500),
    textbox=gr.Textbox(placeholder="Message chatbot", container=False, scale=7),
    theme="soft",
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear"
).launch()