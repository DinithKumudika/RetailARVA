from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from enum import Enum
from uuid import uuid4, UUID


store = {}

class OutputParserTypes(Enum):
    STRING = 1

class GeminiChat:
    def __init__(self, api_key: str, model_id: str = "gemini-1.0-pro") -> None:
        self.model = ChatGoogleGenerativeAI(
            model=model_id, 
            google_api_key=api_key,
            convert_system_message_to_human=True
        )
        self.parse : object | None  = None
        self.system_prompt : str = '''
        You are a helpful virtual sales representative for an retail store. 
        Your primary goal is to assist customers with their inquiries, provide detailed information about products, help them find what they're looking for. Here are some key guidelines to follow:
        [Guidelines]
        - Friendly and Professional Tone: Always maintain a friendly and professional tone. Greet customers warmly and be courteous throughout the conversation.
        - Product Knowledge: Be knowledgeable about all the products listed in the store. Provide accurate and detailed information about the features, prices, and benefits of each product.
        - Customer Assistance: Help customers find products based on their needs and preferences. Offer recommendations and suggest complementary products to enhance their shopping experience.
        - Handling Queries: Respond promptly to customer queries. If a customer has a question about a specific product, provide clear and concise answers.
        - Problem Resolution: Address any issues or concerns the customers might have.
        - Personalization: Personalize interactions by using the customer's name if provided and referencing their past interactions or preferences.
        '''

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    def set_parser(self, parser: OutputParserTypes) -> None:
        if parser == OutputParserTypes.STRING:
            self.parser = StrOutputParser()
    
    def create_new_session() -> UUID:
        return uuid4()
    
    def invoke(self, query: str) -> None:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_prompt),
                MessagesPlaceholder(variable_name="messages")
            ]
        )

        try:
            chain = prompt | self.model | self.parser
            with_message_history = RunnableWithMessageHistory(chain, self.get_session_history, input_messages_key="messages")
            config = {"configurable": {"session_id": f"{self.create_new_session()}"}}
            for r in with_message_history.stream(
                {"messages": [HumanMessage(content=query)]},
                config=config,
            ):
                print(r)
        except Exception as e:
            raise