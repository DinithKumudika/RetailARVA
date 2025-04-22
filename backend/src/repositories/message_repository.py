from src.configs.database import Database
from src.models.entities import Chat, Message
from src.enums import ChatMessageRole

class MessageRepository:
     def __init__(self, db : Database) -> None:
          self.session = db.get_session()

     def fetch_all(self):
          return self.session.query(Message).all()
     
     def add_single(self, chat_id: int, role: ChatMessageRole, content: str):
          new_message = Message(chat_id=chat_id, role=role.value, content=content)
          self.session.add(new_message)
          self.session.commit()
          return new_message

     def get_by_chat_id(self, chat_id: int):
          return self.session.query(Message).filter(Message.chat_id == chat_id).all()