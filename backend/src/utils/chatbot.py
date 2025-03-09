from typing import List
import langchain 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_core.runnables.base import RunnableSerializable
from src.models.models import Message
from src.utils.rag_pipeline import RagPipeline
from src.utils import prompts
from enum import Enum
from src.utils.rag_helper import RagHelper
from src.repositories.message_repository import MessageRepository
from src.repositories.chat_repository import ChatRepository
from src.configs.database import Database
from flask import current_app as app

langchain.debug=True

class OutputParserTypes(Enum):
    STRING = 1


class ChatRoles(Enum):
    ASSISTANT = 1
    USER = 2
    SYSTEM = 3

class Chatbot:
    def __init__(self) -> None:
        self.model = RagHelper().get_llm()
        self.vector_store: QdrantVectorStore | None = None
        self.parser : object | None  = None
        self.contextualize_q_chain = None
        self.session_id = None
        self.formatted_message_history: None | List = None
    
    def serialize_message(self, message):
        if isinstance(message, HumanMessage):
            return {"type": "human", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"type": "ai", "content": message.content}
        else:
            return {"type": "unknown", "content": str(message)}

    def set_parser(self, parser: OutputParserTypes) -> None:
        if parser == OutputParserTypes.STRING:
            self.parser = StrOutputParser()

    def set_vector_store(self, vector_store : QdrantVectorStore):
        self.vector_store = vector_store
    
    def format_docs(self, docs : List[Document]):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def contextualized_question(self, input: dict):
        if input.get("chat_history"):
            return self.contextualize_q_chain
        else:
            return input["question"]
        
    def print_chat_history(self, messages: list):
        for message in messages:
            print(f"{message.role}: {message.content}")
            
    def format_to_message_history(self, chat_history:list[Message]) -> list:
        formated_history = []
        for message in chat_history:
            if message.role == "assistant":
                formated_history.append(AIMessage(content=message.content))
            elif message.role == "user":
                formated_history.append(HumanMessage(content=message.content))
        return formated_history
    
    def greet(self) -> str:
        prompt = PromptTemplate.from_template(f"{prompts.system_prompt}\n{prompts.greet_prompt}")
        llm_chain : RunnableSerializable = prompt | self.model | self.parser
        response = llm_chain.invoke({})
        return response
    
    def invoke(self, query: str, chat_history: list) -> str:
        try:
            rag_pipeline: RagPipeline = app.config['RAG_PIPELINE']()
            response = rag_pipeline.invoke(query, chat_history)    
            return response
        except Exception as e:
            print(e)
            raise