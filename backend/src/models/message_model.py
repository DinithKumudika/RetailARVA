from pydantic import BaseModel
from typing import List, Optional

class MessageModel(BaseModel):
     id : int
     role : str
     content : str
     chat_id : int