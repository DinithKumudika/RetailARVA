from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.prompts import Prompts
from  langchain_core.prompts.chat import HumanMessagePromptTemplate

from enum import Enum
from uuid import uuid4, UUID

store = {}

class OutputParserTypes(Enum):
    STRING = 1


class ChatRoles(Enum):
    ASSISTANT = 1
    USER = 2
    SYSTEM = 3

class GeminiChat:
    def __init__(self, api_key: str, model_id: str = "gemini-1.0-pro") -> None:
        self.model = ChatGoogleGenerativeAI(
            model=model_id, 
            google_api_key=api_key,
            convert_system_message_to_human=True
        )
        self.vector_store: QdrantVectorStore | None = None
        self.parser : object | None  = None
        self.contextualize_q_chain = None
        self.chatHistory = []

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    def get_chat_history(self):
        return self.chatHistory
    
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
    
    def invoke(self, query: str) -> str:
        
        try:

            retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

            # retriever.get_relevant_documents(query=query)
            docs = retriever.invoke(input=query)
            print(f"Retrieved Context: \n{self.format_docs(docs)}")

            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=Prompts.contextualize_q_system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{question}")
                    # HumanMessage(content=f"{question}"),
                ]
            )

            contextualize_q_chain = contextualize_q_prompt | self.model | self.parser

            # history_aware_retriever = create_history_aware_retriever(
            #     self.model, 
            #     retriever, 
            #     contextualize_q_prompt
            # )

            session_id : str = str(self.create_new_session())
            print(f"session id of new sesion: {session_id}")
            print(f"session history: {self.get_session_history(session_id=session_id)}")

            contextualize_q_chain.invoke(
                {
                    "chat_history": self.chatHistory,
                    "question": query,
                }
            )

            # qa_system_prompt = PromptTemplate.from_template(Prompts.qa_system_prompt_template)

            # print(f"QA system prompt: {qa_system_prompt}")

            rag_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=f"{Prompts.system_prompt}\n{Prompts.qa_system_prompt}"),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{question}"),
                    # HumanMessage(content=f"{question}"),
                ]
            )

            rag_chain = (
                RunnablePassthrough.assign(
                    context = self.contextualized_question | retriever | self.format_docs
                )
                | rag_prompt
                | self.model
            )

            print(f"RAG Prompt: \n {rag_prompt}")

            print(f"Chat History: {self.chatHistory}")

            response = rag_chain.invoke({
                    "question": query,
                    "chat_history": self.chatHistory
                }
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