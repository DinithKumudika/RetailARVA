import gradio as gr
from dotenv import dotenv_values
from gradio import ChatMessage
from utils.vector_db import VectorDb
from utils.chatbot import Chatbot, OutputParserTypes
from langchain_core.messages import HumanMessage, AIMessage

env = dotenv_values("../.env")

def qdrant_init():
    qdrant = VectorDb(
        env.get('QDRANT_CLUSTER_URL'), 
        env.get('QDRANT_API_KEY')
    )
    qdrant.set_embedding_model(model_id="llama3.1")
    return qdrant

def chat_init():
    gemini_chat = Chatbot(model_id="llama3.1")
    gemini_chat.set_parser(OutputParserTypes.STRING)
    
    qdrant = qdrant_init()
    gemini_chat.set_vector_store(qdrant.get_collection("products"))
    return gemini_chat

gemini_chat = chat_init()

def greet_user():
    greeting = gemini_chat.greet()
    gemini_chat.chatHistory.append(AIMessage(content=greeting))
    return greeting


def chat_fucntion(message, history: list):
    chat_response = gemini_chat.invoke(message)
    gemini_chat.chatHistory.append(HumanMessage(content=message))
    gemini_chat.chatHistory.append(AIMessage(content=chat_response))
    print(f"Chat History: {gemini_chat.get_chat_history()}")

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
).launch(share=True)