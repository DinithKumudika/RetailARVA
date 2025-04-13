from datetime import datetime
from bson.objectid import ObjectId
from src.enums import Gender

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
            benefits: list,
            is_natural: bool,
            concentrations: list,
            usage: str,
            application_tips: str,
            skin_types: list,
            skin_concerns: list,
            average_rating: float,
            customer_reviews: list,
            expert_review: str,
            claims: list,
            for_sensitive_skin: str,
            allergens: list | None = None,
            side_effects: list | None = None,
            _id=None,
    ):
        self.id = _id if _id else ObjectId()
        self.product_id = product_id
        self.name = name
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
        self.average_rating = average_rating
        self.customer_reviews = customer_reviews
        self.expert_review = expert_review
        self.claims = claims
        self.for_sensitive_skin = for_sensitive_skin

    def to_dict(self):
        """
        Converts the Product object into a dictionary for MongoDB.
        """
        return {
            "_id": self.id,
            "product_id": self.product_id,
            "name": self.name,
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
            "average_rating": self.average_rating,
            "customer_reviews": self.customer_reviews,
            "expert_review": self.expert_review,
            "claims": self.claims,
            "for_sensitive_skin": self.for_sensitive_skin,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Product object from a dictionary (e.g., retrieved from MongoDB).
        """
        return Product(
            _id=data.get("_id"),
            product_id=data.get("product_id", data.get("Id")),  # Handle JSON's "Id" field
            name=data.get("name", data.get("Name")),  # Handle JSON's "Name" field
            brand=data.get("brand", data.get("Brand")),  # Handle JSON's "Brand" field
            category=data.get("category", data.get("Category")),  # Handle JSON's "Category" field
            price=data.get("price"),
            ingredients=data.get("ingredients", data.get("Ingredients")),  # Handle JSON's "Ingredients"
            key_ingredients=data.get("key_ingredients", data.get("Key Ingredients")),  # Handle JSON's "Key Ingredients"
            benefits=data.get("benefits", data.get("Benefits")),  # Handle JSON's "Benefits"
            side_effects=data.get("side_effects", data.get("Potential Side Effects")),
            # Handle JSON's "Potential Side Effects"
            is_natural=data.get("is_natural", data.get("Natural")),  # Handle JSON's "Natural"
            concentrations=data.get("concentrations", data.get("Concentrations")),  # Handle JSON's "Concentrations"
            usage=data.get("usage", data.get("Usage")),  # Handle JSON's "Usage"
            application_tips=data.get("application_tips", data.get("Application Tips")),
            # Handle JSON's "Application Tips"
            skin_types=data.get("skin_types", data.get("Skin Type")),  # Handle JSON's "Skin Type"
            skin_concerns=data.get("skin_concerns", data.get("Skin Concerns")),  # Handle JSON's "Skin Concerns"
            allergens=data.get("allergens", data.get("Allergens")),  # Handle JSON's "Allergens"
            average_rating=data.get("average_rating", data.get("Average Rating")),  # Handle JSON's "Average Rating"
            customer_reviews=data.get("customer_reviews", data.get("Customer Reviews")),
            # Handle JSON's "Customer Reviews"
            expert_review=data.get("expert_review", data.get("Expert Review")),  # Handle JSON's "Expert Review"
            claims=data.get("claims", data.get("Claims")),  # Handle JSON's "Claims"
            for_sensitive_skin=data.get("for_sensitive_skin", data.get("For Sensitive Skin")),
            # Handle JSON's "For Sensitive Skin"
        )

    def __repr__(self):
        return f"Product(name='{self.name}', brand='{self.brand}', category='{self.category}')"
    
class User:
    def __init__(self, first_name : str, last_name : str, email: str, _id=None, created_at=None):
        self.id = _id if _id else ObjectId()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = created_at if created_at else datetime.utcnow()
    
    def to_dict(self):
        """
        Converts the User object into a dictionary for MongoDB.
        """
        return {
            "_id": self.id,
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

class UserProfile:
    def __init__(self, user_id: str, age: int, gender: str, skin_type: str, sensitive_skin: bool, skin_concerns: list[str], ingredients_to_avoid: list[str], known_allergies: list[str], min_price: float, max_price: float, preferences: list[str], _id = None, created_at = None):
        self.id = _id if _id else ObjectId()
        self.user_id = ObjectId(user_id)
        self.created_at = created_at if created_at else datetime.utcnow()
        self.age = age
        self.gender =  Gender.MALE.value if gender == "Male" else Gender.FEMALE.value
        self.skin_type = skin_type
        self.sensitive_skin = sensitive_skin
        self.skin_concerns = skin_concerns
        self.ingredients_to_avoid = ingredients_to_avoid
        self.known_allergies = known_allergies
        self.min_price = min_price
        self.max_price = max_price
        self.preferences = preferences

    def to_dict(self):
        """
        Converts the UserProfile object into a dictionary for MongoDB.
        """
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender,
            "skin_type": self.skin_type,
            "sensitive_skin": self.sensitive_skin,
            "skin_concerns": self.skin_concerns,
            "ingredients_to_avoid": self.ingredients_to_avoid,
            "known_allergies": self.known_allergies,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "preferences": self.preferences,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a UserProfile object from a dictionary (e.g., retrieved from MongoDB).
        """
        return UserProfile(
            _id=data.get("_id"),
            user_id=data.get("user_id"),
            age=data.get("age"),
            gender=data.get("gender"),
            skin_type=data.get("skin_type"),
            sensitive_skin=data.get("sensitive_skin"),
            skin_concerns=data.get("skin_concerns"),
            ingredients_to_avoid=data.get("ingredients_to_avoid"),
            known_allergies=data.get("known_allergies"),
            min_price=data.get("min_price"),
            max_price=data.get("max_price"),
            preferences=data.get("preferences"),
            created_at=data.get("created_at")
        )

    def __repr__(self):
        return f"UserProfile(_id='{self.id}', user_id='{self.user_id}')"

class Chat:
    def __init__(self, user_id: str, messages_count: int = 0, _id=None, created_at=None):
        self.id: ObjectId = _id if _id else ObjectId()  # MongoDB uses `_id` as the primary key
        self.user_id: ObjectId = ObjectId(user_id)
        self.messages_count: int = messages_count
        self.created_at = created_at if created_at else datetime.utcnow()  # Timestamp for creation

    def to_dict(self):
        """
        Converts the Chat object into a dictionary for MongoDB.
        """
        return {
            "_id": self.id,
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
        return f"Chat(_id='{self.id}', user_id='{self.user_id}', messages_count={self.messages_count})"
        

class Message:
    def __init__(self, chat_id: ObjectId, role: str, content: str, message_id: int, _id=None):
        self.id: ObjectId = _id if _id else ObjectId()  # MongoDB uses `_id` as the primary key
        self.chat_id: ObjectId = chat_id  # Reference to the parent chat
        self.message_id: int = message_id
        self.role: str = role
        self.content: str = content

    def to_dict(self):
        """
        Converts the Message object into a dictionary for MongoDB.
        """
        return {
            "_id": self.id,
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