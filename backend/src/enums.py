from enum import Enum

class ChatMessageRole(Enum):
     USER = "user"
     ASSISTANT = "assistant"
     SYSTEM = "system"

class Gender(Enum):
     MALE = "Male"
     FEMALE = "Female"