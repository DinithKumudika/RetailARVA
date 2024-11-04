from typing import List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_core.runnables.base import RunnableSerializable
from langchain.memory import ConversationBufferWindowMemory
from utils import prompts
from enum import Enum
from uuid import uuid4, UUID
from utils.rag_helper import RagHelper
from enums import ChatMessageRole
from repositories.message_repository import MessageRepository
from repositories.chat_repository import ChatRepository
from configs.database import Database


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

    def get_session_history(self, session_id: int) -> list:
        chat_messages = self.message_store.get_by_chat_id(session_id)
        
        if not chat_messages:
            chat = self.chat_repo.add_single()
            return self.message_store.get_by_chat_id(chat.chat_id)
        else:
            return chat_messages
        # if session_id not in session_store:
        #     session_store[session_id] = InMemoryChatMessageHistory()
        # return session_store[session_id]
    
    def serialize_message(self, message):
        if isinstance(message, HumanMessage):
            return {"type": "human", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"type": "ai", "content": message.content}
        else:
            return {"type": "unknown", "content": str(message)}
    
    def add_message_to_history(self, message : str, role: ChatRoles):
        if role.name == ChatRoles.ASSISTANT:
            self.chatHistory.append(AIMessage(content=message))
        elif role.name == ChatRoles.USER:
            self.chatHistory.append(HumanMessage(content=message))

    def set_parser(self, parser: OutputParserTypes) -> None:
        if parser == OutputParserTypes.STRING:
            self.parser = StrOutputParser()

    def set_vector_store(self, vector_store : QdrantVectorStore):
        self.vector_store = vector_store
    
    def create_new_session(self) -> UUID:
        return uuid4()
    
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
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessage(content=f"{Prompts.system_prompt}\n{Prompts.greet_prompt}"),
        #     ]
        # )
        self.session_id = 1
        chat_session = self.get_session_history(session_id=self.session_id)
        
        prompt = PromptTemplate.from_template(f"{prompts.system_prompt}\n{prompts.greet_prompt}")
        llm_chain : RunnableSerializable = prompt | self.model | self.parser

        response = llm_chain.invoke({})
        
        self.message_store.add_single(
            chat_id=self.session_id, 
            role=ChatMessageRole.ASSISTANT, 
            content=response
        )

        return response

    
    def invoke(self, query: str) -> str:
        self.message_store.add_single(
            chat_id=self.session_id, 
            role=ChatMessageRole.USER, 
            content=query
        )
        
        chat_session = self.get_session_history(self.session_id)
        self.print_chat_history(chat_session)
        formatted_messages = self.format_to_message_history(chat_session)
        print(f"length of chat history: {len(formatted_messages)}")
        
        try:
            retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

            # docs = retriever.get_relevant_documents(query=query)
            docs = retriever.invoke(input=query)
            # print(f"Retrieved Context: \n{self.format_docs(docs)}")

            # contextualize_q_prompt = ChatPromptTemplate.from_messages(
            #     [
            #         SystemMessage(content=Prompts.contextualize_q_system_prompt),
            #         MessagesPlaceholder(variable_name="chat_history"),
            #         # HumanMessagePromptTemplate.from_template("question: {question}"),
            #         HumanMessage(content="question: {question}"),
            #     ]
            # )

            # formatted_contextualize_q_prompt = contextualize_q_prompt.format(
            #     chat_history=self.chatHistory, 
            #     question=query
            # )
            # print(f"Contextualize Q Prompt: \n{formatted_contextualize_q_prompt}")
            # print("\nEnd of Contextualize Q Prompt\n")

            # self.contextualize_q_chain = contextualize_q_prompt | self.model | self.parser

            # history_aware_retriever = create_history_aware_retriever(
            #     self.model, 
            #     retriever, 
            #     contextualize_q_prompt
            # )
            
            # contextualize_q = self.contextualize_q_chain.invoke(
            #     {
            #         "chat_history": self.chatHistory,
            #         "question": query,
            #     }
            # )
            
            # print(f"contextualized question: {contextualize_q}")
            
            rag_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=f"{prompts.system_prompt}\n{prompts.qa_system_prompt_updated}"),
                    MessagesPlaceholder(variable_name="chat_history"),
                    # HumanMessagePromptTemplate.from_template("question: {question}"),
                    HumanMessage(content="{question}"),
                ]
            )
            
            # Render and print the RAG prompt
            formatted_rag_prompt = rag_prompt.format(
                chat_history=formatted_messages, 
                question=query,
                context=self.format_docs(docs)
            )
            # print(f"RAG Prompt: \n{formatted_rag_prompt}")
            # print("\nEnd of RAG Prompt\n")

            rag_chain = rag_prompt | self.model | self.parser
            
            # rag_chain = (
            #     {
            #         "context": retriever | self.format_docs,
            #         "question": RunnablePassthrough(),
            #         "chat_history": RunnablePassthrough()
            #     }
            #     | rag_prompt
            #     | self.model
            #     | self.parser
            # )

            response = rag_chain.invoke({
                    "question": query,
                    "chat_history": formatted_messages
                }
            )
            
            print(f"bot response: {response}")
            
            self.message_store.add_single(
                chat_id=self.session_id, 
                role=ChatMessageRole.ASSISTANT, 
                content=response
            )

            return response

            # print(f"QA system prompt: {qa_system_prompt}")

            # rag_prompt = ChatPromptTemplate.from_messages(
            #     [
            #         SystemMessage(content=f"{Prompts.system_prompt}\n{Prompts.qa_system_prompt_template}"),
            #         MessagesPlaceholder(variable_name="chat_history"),
            #         HumanMessagePromptTemplate.from_template("{input}"),
            #     ]
            # )

            # print(f"RAG prompt: \n {rag_prompt}")

            # question_answer_chain = create_stuff_documents_chain(self.model, rag_prompt)
            # rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

            # coversational_rag_chain = RunnableWithMessageHistory(
            #     rag_chain, 
            #     self.get_session_history, 
            #     input_messages_key="input",
            #     history_messages_key="chat_history",
            #     output_messages_key="answer"
            # )

            # session_id : str = str(self.create_new_session())

            # result = contextualize_q_chain.invoke(
            #     {"input": query},
            #     config={"configurable": {"session_id": f"{session_id}"}},
            # )["answer"]

            # print(result)
        
        # rag_chain = (
            #     {"context": retriever | self.format_docs , "question": RunnablePassthrough()}
            #     | rag_prompt
            #     | self.model
            #     | self.parser
            # )

            # rag_chain_with_parser = RunnableMap(
            #     {
            #         "output": rag_chain,
            #         "parsed_output": self.parser,
            #     }
            # )
            
        except Exception as e:
            raise