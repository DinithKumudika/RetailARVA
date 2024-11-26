from typing import List
import langchain 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_core.runnables.base import RunnableSerializable
from utils.rag_pipeline import RagPipeline
from utils import prompts
from enum import Enum
from utils.rag_helper import RagHelper
from enums import ChatMessageRole
from repositories.message_repository import MessageRepository
from repositories.chat_repository import ChatRepository
from configs.database import Database

langchain.debug=True

class OutputParserTypes(Enum):
    STRING = 1


class ChatRoles(Enum):
    ASSISTANT = 1
    USER = 2
    SYSTEM = 3

class Chatbot:
    def __init__(self, db: Database) -> None:
        self.model = RagHelper().get_llm()
        self.vector_store: QdrantVectorStore | None = None
        self.parser : object | None  = None
        self.contextualize_q_chain = None
        self.message_store = MessageRepository(db)
        self.chat_repo = ChatRepository(db)
        self.session_id = None
        self.formatted_message_history: None | List = None
        self.chat_history = []
    
    def serialize_message(self, message):
        if isinstance(message, HumanMessage):
            return {"type": "human", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"type": "ai", "content": message.content}
        else:
            return {"type": "unknown", "content": str(message)}
    
    def add_message_to_history(self, message : str, role: ChatRoles):
        if role.name == ChatRoles.ASSISTANT:
            self.chat_history.extend(AIMessage(content=message))
        elif role.name == ChatRoles.USER:
            self.chat_history.extend(HumanMessage(content=message))

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
            
    def format_to_message_history(self, chat_messages) -> list:
        messages = []
        for message in chat_messages:
            if message.role == ChatMessageRole.ASSISTANT.value:
                messages.append(AIMessage(content=message.content))
            elif message.role == ChatMessageRole.USER.value:
                messages.append(HumanMessage(content=message.content))
        return messages
    
    def greet(self) -> str:
        prompt = PromptTemplate.from_template(f"{prompts.system_prompt}\n{prompts.greet_prompt}")
        llm_chain : RunnableSerializable = prompt | self.model | self.parser

        response = llm_chain.invoke({})
        self.add_message_to_history(response, ChatMessageRole.ASSISTANT)
        return response

    
    def invoke(self, query: str, rag_pipeline: RagPipeline) -> str:
        try:
            response = rag_pipeline.invoke(query, self.chat_history)
            
            self.add_message_to_history(query, ChatMessageRole.USER)
            self.add_message_to_history(response, ChatMessageRole.ASSISTANT)
            
            return response
        except Exception as e:
            raise