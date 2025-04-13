class NoProductsFoundError(Exception):
    """Custom exception for when no products are found in the database."""
    def __init__(self, message="No products found in the database"):
        self.message = message
        super().__init__(self.message)
        
class ProductNotFoundError(Exception):
    """Custom exception for when a product is not found in the database."""
    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"No product found with id: {product_id}")

class UserInsertionError(Exception):
    """Custom exception for errors during user insertion."""
    def __init__(self, message: str="User insertion failed: Operation not acknowledged."):
        self.message = message
        super().__init__(self.message)

class ProfileDataInsertionError(Exception):
    """Custom exception for errors during profile data insertion."""
    def __init__(self, message: str="Profile data insertion failed: Operation not acknowledged."):
        self.message = message
        super().__init__(self.message)
        
class ProductInsertionError(Exception):
    """Custom exception for errors during product insertion."""
    def __init__(self, message: str="Product insertion failed: Operation not acknowledged."):
        self.message = message
        super().__init__(message)
        
class UserNotFoundError(Exception):
    """Custom exception for when a user is not found in the database."""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"No user found with id: {user_id}")
        
class ChatNotFoundError(Exception):
    """Custom exception for when a chat is not found in the database."""
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        super().__init__(f"No chat found with id: {chat_id}")
        
class ChatCreationError(Exception):
    """Custom exception for errors during chat creation."""
    def __init__(self, message: str = "Chat insertion failed: Operation not acknowledged."):
        self.message = message
        super().__init__(message)
        
class ChatUpdateError(Exception):
    """Custom exception for errors during chat updates."""
    def __init__(self, message: str):
        super().__init__(message)

class ChatHistoryNotFoundError(Exception):
    """Custom exception for when no chat history is found."""
    def __init__(self, chat_id: str):
        super().__init__(f"No chat history found for chat ID: {chat_id}")
        
class MessageInsertionError(Exception):
    """Custom exception for errors during message insertion."""
    def __init__(self, message: str = "Message insertion was not acknowledged by the database."):
        self.message = message
        super().__init__(message)