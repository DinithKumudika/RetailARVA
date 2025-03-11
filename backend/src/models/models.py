from datetime import datetime
from bson.objectid import ObjectId

class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        brand: str,
        category: str,
        price: float,
        ingredients: list,
        key_ingredients: list,
        benefits: str,
        is_natural: bool,
        concentrations: str,
        usage: str,
        application_tips: str,
        skin_types: str,
        skin_concerns: list,
        allergens: list | None = None,
        side_effects: str | None = None,
        sensitivities: str| None = None,
        _id=None,
    ):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.id = product_id
        self.brand = brand
        self.category = category
        self.price = price
        self.ingredients = ingredients
        self.key_ingredients = key_ingredients
        self.benefits = benefits
        self.side_effects = side_effects
        self.is_natural = is_natural
        self.concentrations = concentrations
        self.usage = usage
        self.application_tips = application_tips
        self.skin_types = skin_types
        self.skin_concerns = skin_concerns
        self.allergens = allergens
        self.sensitivities = sensitivities

    def to_dict(self):
        """
        Converts the Product object into a dictionary for MongoDB.
        """
        return {
            "_id": self._id,
            "name": self.name,
            "product_id": self.id,
            "brand": self.brand,
            "category": self.category,
            "price": self.price,
            "ingredients": self.ingredients,
            "key_ingredients": self.key_ingredients,
            "benefits": self.benefits,
            "side_effects": self.side_effects,
            "is_natural": self.is_natural,
            "concentrations": self.concentrations,
            "usage": self.usage,
            "application_tips": self.application_tips,
            "skin_types": self.skin_types,
            "skin_concerns": self.skin_concerns,
            "allergens": self.allergens,
            "sensitivities": self.sensitivities,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Product object from a dictionary (e.g., retrieved from MongoDB).
        """
        print(data.get("product_id"))
        return Product(
            _id=data.get("_id"),
            product_id=data.get("product_id"),
            name=data.get("name"),
            brand=data.get("brand"),
            category=data.get("category"),
            price=data.get("price"),
            ingredients=data.get("ingredients"),
            key_ingredients=data.get("key_ingredients"),
            benefits=data.get("benefits"),
            side_effects=data.get("side_effects"),
            is_natural=data.get("is_natural"),
            concentrations=data.get("concentrations"),
            usage=data.get("usage"),
            application_tips=data.get("application_tips"),
            skin_types=data.get("skin_types"),
            skin_concerns=data.get("skin_concerns"),
            allergens=data.get("allergens"),
            sensitivities=data.get("sensitivities"),
        )

    def __repr__(self):
        return f"Product(name='{self.name}', brand='{self.brand}', category='{self.category}')"

class CustomerReview:
    def __init__(self, product_id, review, rating, _id=None):
        self._id = _id if _id else ObjectId()
        self.product_id = ObjectId(product_id) 
        self.review = review
        self.rating = rating

    def to_dict(self):
        """
        Converts the CustomerReview object into a dictionary for MongoDB.
        """
        return {
            "_id": self._id,
            "product_id": self.product_id,
            "review": self.review,
            "rating": self.rating,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a CustomerReview object from a dictionary (e.g., retrieved from MongoDB).
        """
        return CustomerReview(
            _id=data.get("_id"),
            product_id=data.get("product_id"),
            review=data.get("review"),
            rating=data.get("rating"),
        )

    def __repr__(self):
        return f"CustomerReview(product_id='{self.product_id}', rating={self.rating})"       
    
class User:
    def __init__(self, first_name : str, last_name : str, email: str, _id=None, created_at=None):
        self._id = _id if _id else ObjectId()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = created_at if created_at else datetime.utcnow()
    
    def to_dict(self):
        """
        Converts the User object into a dictionary for MongoDB.
        """
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at
        }  
        
    @staticmethod
    def from_dict(data):
        """
        Creates a User object from a dictionary (e.g., retrieved from MongoDB).
        """
        return User(
            _id=data.get("_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            created_at=data.get("created_at"),
        )
    
    def __repr__(self):
        return f"User(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"

class Chat:
    def __init__(self, user_id: str, messages_count: int = 0, _id=None, created_at=None):
        self._id: ObjectId = _id if _id else ObjectId()  # MongoDB uses `_id` as the primary key
        self.user_id: ObjectId = ObjectId(user_id)
        self.messages_count: int = messages_count
        self.created_at = created_at if created_at else datetime.utcnow()  # Timestamp for creation

    def to_dict(self):
        """
        Converts the Chat object into a dictionary for MongoDB.
        """
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "messages_count": self.messages_count,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Chat object from a dictionary (e.g., retrieved from MongoDB).
        """
        return Chat(
            _id=data.get("_id"),
            user_id=data.get("user_id"),
            messages_count=data.get("messages_count"),
            created_at=data.get("created_at"),
        )

    def __repr__(self):
        return f"Chat(_id='{self._id}', user_id='{self.user_id}', messages_count={self.messages_count})"
        

class Message:
    def __init__(self, chat_id: ObjectId, role: str, content: str, message_id: int, _id=None):
        self._id: ObjectId = _id if _id else ObjectId()  # MongoDB uses `_id` as the primary key
        self.chat_id: ObjectId = chat_id  # Reference to the parent chat
        self.message_id: int = message_id
        self.role: str = role
        self.content: str = content

    def to_dict(self):
        """
        Converts the Message object into a dictionary for MongoDB.
        """
        return {
            "_id": self._id,
            "chat_id": self.chat_id,
            "role": self.role,
            "message_id": self.message_id,
            "content": self.content,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Message object from a dictionary (e.g., retrieved from MongoDB).
        """
        return Message(
            _id=data.get("_id"),
            chat_id=data.get("chat_id"),
            role=data.get("role"),
            message_id=data.get("message_id"),
            content=data.get("content"),
        )

    def __repr__(self):
        return f"Message(chat_id='{self.chat_id}', role='{self.role}', message_id='{self.message_id}')"