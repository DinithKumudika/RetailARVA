import langchain
from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnablePassthrough, RunnableWithMessageHistory
from src.utils.chains import classification_chain_invoke, get_recommendation_chain, \
    get_product_info_chain, get_suitability_chain, get_default_chain, get_greet_chain
from enum import Enum
from src.utils.rag_helper import RagHelper
from flask import current_app as app
from langchain.globals import set_debug

langchain.debug=True
set_debug(True)


class ChatRoles(Enum):
    ASSISTANT = 1
    USER = 2
    SYSTEM = 3

class Chatbot:
    def __init__(self) -> None:
        self.llm = RagHelper().get_llm()
        self.session_id: str| None = None
        self.chat_session: MongoDBChatMessageHistory | None = None

    def set_chat_session(self):
        config = app.config
        self.chat_session = MongoDBChatMessageHistory(
            session_id=self.session_id,
            connection_string=f"mongodb://{config.get('MONGO_HOST')}:{config.get('MONGO_PORT')}",
            database_name=config.get('MONGO_DBNAME'),
            collection_name="chat_sessions"
        )

    def get_chat_session(self) -> MongoDBChatMessageHistory:
        """
        Dynamically fetch or create a chat session for the given session_id.

        Returns:
            MongoDBChatMessageHistory: A chat session object with messages stored in MongoDB.
        """
        # Fetch MongoDB connection details from the app configuration
        config = app.config

        # Create and return a MongoDBChatMessageHistory instance for the session_id
        return MongoDBChatMessageHistory(
            session_id=self.session_id,
            connection_string=f"mongodb://{config['MONGO_HOST']}:{config['MONGO_PORT']}",
            database_name=config['MONGO_DBNAME'],
            collection_name="chat_sessions"
        )

    def add_user_message(self, message: str):
        if self.chat_session is None:
            raise ValueError("Chat session is not set. Call set_chat_session() first.")

        self.chat_session.add_user_message(message)

    def add_ai_message(self, message: str):
        if self.chat_session is None:
            raise ValueError("Chat session is not set. Call set_chat_session() first.")

        self.chat_session.add_ai_message(message)

    def get_chat_history(self):
        if self.chat_session is None:
            raise ValueError("Chat session is not set. Call set_chat_session() first.")

        return self.chat_session.messages

    @staticmethod
    def route(query: str):
        classification_model = RagHelper.get_classification_model()

        result = classification_chain_invoke(classification_model, query)

        if "suitability_check" in result:
            return "suitability_check"
        if "recommendation" in result:
            return "recommendation"
        if "product_info" in result:
            return "product_info"
        else:
            return "general"
    
    def greet(self, user_name: str) -> str:
        greet_chain = get_greet_chain(self.llm)
        response = greet_chain.invoke({"user": user_name})
        self.add_ai_message(response)
        return response
    
    def invoke(self, query: str, user_id: str, product_id: int) -> str:
        try:
            product_info_chain = get_product_info_chain(self.llm)
            product_info_chain_with_history = RunnableWithMessageHistory(
                product_info_chain,
                lambda session_id: self.chat_session,
                input_messages_key="query",
                history_messages_key="chat_history",
            )

            suitability_chain = get_suitability_chain(self.llm)
            suitability_chain_with_history = RunnableWithMessageHistory(
                suitability_chain,
                lambda session_id: self.chat_session,
                input_messages_key="query",
                history_messages_key="chat_history",
            )

            recommendation_chain = get_recommendation_chain(self.llm)
            recommendation_chain_with_history = RunnableWithMessageHistory(
                recommendation_chain,
                lambda session_id: self.chat_session,
                input_messages_key="query",
                history_messages_key="chat_history"
            )

            default_chain = get_default_chain(self.llm)
            default_chain_with_history = RunnableWithMessageHistory(
                default_chain,
                lambda session_id: self.chat_session,
                input_messages_key="query",
                history_messages_key="chat_history"
            )

            routed_chain = RunnableBranch(
                # Route to product_info_chain if the classification is "product_info"
                (lambda inputs: inputs["classification"] == "product_info", product_info_chain_with_history),
                # Route to suitability_chain if the classification is "suitability_check"
                (lambda inputs: inputs["classification"] == "suitability_check", suitability_chain_with_history),
                # Route to recommendation_chain if the classification is "recommendation"
                (lambda inputs: inputs["classification"] == "recommendation", recommendation_chain_with_history),
                default_chain_with_history
            )

            print(f"query to the routing: {query}")
            routing_function = RunnableLambda(lambda inputs: Chatbot.route(inputs["query"]))

            full_chain = (
                {
                    "classification": routing_function,
                    "query": lambda inputs: inputs["query"],
                    "product_info": lambda inputs: inputs["product_info"],
                    "user_info": lambda inputs: inputs["user_info"],
                    "chat_history": lambda inputs: inputs["chat_history"]
                }
                | routed_chain
            )

            user_info = RagHelper.get_formatted_user_profile(user_id)
            print(f"user info:\n {user_info}")

            product_info = RagHelper.get_formatted_product(product_id)
            print(f"product info:\n {product_info}")

            response = full_chain.invoke(
                {
                    "query": query,
                    "product_info": product_info,
                    "user_info": user_info,
                    "chat_history": self.chat_session.messages
                },
                config={"configurable": {"session_id": self.session_id}}
            )
            return response

        except Exception as e:
            print(e)
            raise