from sqlalchemy import Column, String, Integer, CHAR, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    ingredients = Column(String, nullable=False)
    key_ingredients = Column(String, nullable=False)
    benefits = Column(String, nullable=False)
    side_effects = Column(String, nullable=True)
    is_natural = Column(Boolean, nullable=False)
    concentrations = Column(String, nullable=False)
    usage = Column(String, nullable=False)
    application_tips = Column(String, nullable=False)
    skin_types = Column(String, nullable=False)
    skin_concerns = Column(String, nullable=False)
    allergens = Column(String, nullable=True)
    sensitivities  = Column(String, nullable=True)

    def __init__(self, name, brand, category, price, ingredients, key_ingredients, benefits, is_natural, concentrations, usage, application_tips, skin_types, skin_concerns, side_effects = None, allergens = None, sensitivities = None) -> None:
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
        self.sensitivities = sensitivities
    
    def to_dict(self):
        """
        Converts the SQLAlchemy model instance into a dictionary.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class CustomerReview(Base):
    __tablename__ = "customer_reviews"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    review = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    def __init__(self, product_id, review, rating):
        self.product_id = product_id
        self.review = review
        self.rating = rating
        

class Chat(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    messages_count = Column(Integer)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Define relationship to access messages linked to a chat
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    
    def __init__(self, messages_count):
        self.messages_count = messages_count
        

class Message(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    chat = relationship("Chat", back_populates="messages")

    def __init__(self, chat_id, role, content):
        self.chat_id = chat_id
        self.role = role
        self.content = content