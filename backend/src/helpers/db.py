from src.models.models import Product, User, Chat, Message
from flask import current_app as app
from src.exceptions.exceptions import NoProductsFoundError, ProductNotFoundError, UserInsertionError, ProductInsertionError, UserNotFoundError, ChatNotFoundError, ChatCreationError, ChatUpdateError, ChatHistoryNotFoundError, MessageInsertionError
from bson.objectid import ObjectId
from typing import List, Union, Optional
from pymongo.errors import PyMongoError, BulkWriteError


mongo = app.config.get('MONGO')
db = mongo.db

def add_produt(product: Product) -> ObjectId:
    """
    Adds a product to the database.

    Args:
        product (Product): The product object to be added.

    Returns:
        ObjectId: The _id of the inserted product if successful.

    Raises:
        ProductInsertionError: If the insertion fails.
        ValueError: If the product is invalid or cannot be converted to a dictionary.
        PyMongoError: If there is an issue with the database operation.
    """
    try:
        inserted_product = db.products.insert_one(product.to_dict())
        if not inserted_product.acknowledged:
            print("Product insertion failed")
            raise ProductInsertionError()
        return inserted_product.inserted_id
    except AttributeError as e:
        # Handle cases where product.to_dict() fails
        print(f"Invalid product object: {e}")
        raise ValueError(f"Invalid product object: {e}")
    
    except PyMongoError as e:
        # Handle database-related errors
        print(f"Database error while adding product: {e}")
        raise PyMongoError(f"Database error while adding product: {e}")

def add_products(products: list[Product]) -> ObjectId:
    """
    Adds multiple products to the database.

    Args:
        products (List[Product]): A list of Product objects to be added.

    Returns:
        List[ObjectId]: A list of inserted _ids if the operation is successful.

    Raises:
        ProductInsertionError: If the insertion fails.
        ValueError: If the input is invalid or cannot be converted to a list of dictionaries.
        BulkWriteError: If there is an issue during bulk insertion.
        PyMongoError: If there is a general database-related error.
    """
    try:
        product_dicts = [product.to_dict() for product in products]
        result = db.products.insert_many(product_dicts)
        if not result.acknowledged:
            print("Products insertion failed")
            raise ProductInsertionError()
        return result.inserted_ids
    except AttributeError as e:
        print(f"Invalid product object: {e}")
        raise ValueError(f"Failed to convert one or more products to a dictionary: {e}")
    except BulkWriteError as bwe:
        # Handle bulk write errors (e.g., duplicate keys, constraint violations)
        print("Bulk write error while adding products: {bwe.details}")
        raise bwe
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while adding products: {pe}")
        raise pe
    
def get_product_by_id(product_id: int) -> Product:
    """
    Fetches a product from the database by its ID.

    Args:
        product_id (int): The ID of the product to fetch.

    Returns:
        Product: The Product object if found.

    Raises:
        ProductNotFoundError: If no product is found with the given ID.
        PyMongoError: If there is a database-related error.
    """
    try:
        product: Optional[dict] = db.products.find_one({"product_id": product_id})
        if product is None:
            print(f"No product found with id: {product_id}")
            raise ProductNotFoundError(id)
        return Product.from_dict(product)
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while fetching product with id {product_id}: {pe}")
        raise pe

def get_all_products()-> List[Product]:
    """
    Fetches all products from the database.

    Returns:
        List[Product]: A list of Product objects.

    Raises:
        NoProductsFoundError: If no products exist in the database.
    """
    products_cursor = db.products.find()
    products : List[Product] = [Product.from_dict(product) for product in products_cursor]
    if not products:
        print("No products found in the database")
        raise NoProductsFoundError()
    return products

def add_user(user: User) -> ObjectId:
    """
    Adds a user to the database.

    Args:
        user (User): The user object to be added.

    Returns:
        ObjectId: The _id of the inserted user.

    Raises:
        ValueError: If the input is invalid or cannot be converted to a dictionary.
        UserInsertionError: If the insertion is not acknowledged by the database.
        PyMongoError: If there is a database-related error.
    """
    try:
        result = db.users.insert_one(user.to_dict())
        if not result.acknowledged:
            print("user insertion failed")
            raise UserInsertionError()
        return result.inserted_id
    except AttributeError as e:
        # Handle cases where user.to_dict() fails
        print(f"Invalid user object: {e}")
        raise ValueError(f"Failed to convert user to a dictionary: {e}")
    
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while adding user: {pe}")
        raise pe

def get_user_by_id(id: str) -> User:
    """
    Fetches a user from the database by their ID.

    Args:
        id (str): The ID of the user to fetch.

    Returns:
        User: The User object if found.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
        PyMongoError: If there is a database-related error.
    """
    try:
        user: Optional[dict] = db.users.find_one({"_id": ObjectId(id)})
        if user is None:
            print(f"No user found with id: {id}")
            raise UserNotFoundError(id)
        return User.from_dict(user)   
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while fetching user with id {id}: {pe}")
        raise pe

def get_user_by_email(email: str) -> User:
    """
    Fetches a user from the database by their email.

    Args:
        email (str): The email of the user to fetch.

    Returns:
        User: The User object if found.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
        PyMongoError: If there is a database-related error.
    """
    
    try:
        user: Optional[dict] = db.users.find_one({"email": email})
        if user is None:
            print(f"No user found with email: {email}")
            raise UserNotFoundError(email)
        return User.from_dict(user)   
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while fetching user with id {id}: {pe}")
        raise pe
    
def get_chat_by_id(id: str) -> Chat:
    """
    Fetches a chat from the database by its ID.

    Args:
        id (str): The ID of the chat to fetch.

    Returns:
        Chat: The Chat object if found.

    Raises:
        ChatNotFoundError: If no chat is found with the given ID.
        InvalidId: If the provided ID is not a valid ObjectId.
        PyMongoError: If there is a database-related error.
    """
    try:
        chat: Optional[dict] = db.chats.find_one({"_id": ObjectId(id)})
        if chat is None:
            print(f"No chat found with id: {id}")
            raise ChatNotFoundError(id)
        return Chat.from_dict(chat)    
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while fetching chat with id {id}: {pe}")
        raise pe

def create_chat(chat: Chat) -> ObjectId:
    """
    Creates a new chat in the database.

    Args:
        chat (Chat): The chat object to be created.

    Returns:
        ObjectId: The _id of the inserted chat.

    Raises:
        ValueError: If the input is invalid or cannot be converted to a dictionary.
        ChatCreationError: If the insertion is not acknowledged by the database.
        PyMongoError: If there is a database-related error.
    """
    try:
        result = db.chats.insert_one(chat.to_dict())
        if not result.acknowledged:
            print("Chat insertion was not acknowledged by the database.")
            raise ChatCreationError("Chat insertion failed: Operation not acknowledged.")
        return result.inserted_id
    except AttributeError as e:
        # Handle cases where chat.to_dict() fails
        print(f"Invalid chat object: {e}")
        raise ValueError(f"Failed to convert chat to a dictionary: {e}")
    
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while creating chat: {pe}")
        raise pe

def update_message_count(chat_id: str, count: int) -> bool:
    """
    Updates the message count of a chat in the database.

    Args:
        chat_id (str): The ID of the chat to update.
        count (int): The amount by which to increment the message count.

    Returns:
        bool: True if the update was successful, False otherwise.

    Raises:
        ChatUpdateError: If the update operation fails.
        PyMongoError: If there is a database-related error.
    """
    try:
        result = db.chats.update_one(
            {"_id": ObjectId(chat_id)},
            { '$inc' : { "messages_count" : count}}
        )
        
        print(result)
        
        if result.matched_count == 0:
            print(f"No chat found with id: {chat_id}")
            return False
        if result.modified_count == 0:
            print(f"Chat with id {chat_id} was found but not modified.")
            return False
        return True
        
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while updating message count for chat {chat_id}: {pe}")
        raise ChatUpdateError(f"Failed to update message count for chat {chat_id}: {pe}")

def get_chat_history_by_chat_id(chat_id: str) -> list[Message]:
    """
    Fetches the chat history for a given chat ID from the database.

    Args:
        chat_id (str): The ID of the chat to fetch messages for.

    Returns:
        List[Message]: A list of Message objects representing the chat history.

    Raises:
        ValueError: If the input is invalid (e.g., invalid chat_id).
        ChatHistoryNotFoundError: If no messages are found for the given chat ID.
        PyMongoError: If there is a database-related error.
    """
    try:
        chat_mesages_cursor = db.messages.find({"chat_id": ObjectId(chat_id)})
        chat_messages = [Message.from_dict(message) for message in chat_mesages_cursor]
        if not chat_messages:
            print(f"No chat history found for chat ID: {chat_id}")
            raise ChatHistoryNotFoundError(chat_id)
        return chat_messages
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while fetching chat history for chat ID {chat_id}: {pe}")
        raise pe

def add_chat_message(message: Message) -> ObjectId:
    """
    Adds a chat message to the database.

    Args:
        message (Message): The message object to be added.

    Returns:
        ObjectId: The _id of the inserted message.

    Raises:
        MessageInsertionError: If the insertion is not acknowledged by the database.
        PyMongoError: If there is a database-related error.
    """
    try:
        result = db.messages.insert_one(message.to_dict())
        if not result.acknowledged:
            print("Message insertion was not acknowledged by the database.")
            raise MessageInsertionError()
        result.inserted_id
    except AttributeError as e:
        # Handle cases where message.to_dict() fails
        print(f"Invalid message object: {e}")
        raise ValueError(f"Failed to convert message to a dictionary: {e}")
    
    except PyMongoError as pe:
        # Handle general database-related errors
        print(f"Database error while inserting message: {pe}")
        raise pe
    
    
    