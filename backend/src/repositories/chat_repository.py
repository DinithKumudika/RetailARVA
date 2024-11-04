from configs.database import Database
from models.entities import Chat

class ChatRepository:
     def __init__(self, db : Database) -> None:
          self.session = db.get_session()

     def fetch_all(self):
          return self.session.query(Chat).all()
     
     def add_single(self):
          # Create a new Chat instance
          new_chat = Chat(messages_count=0)
          self.session.add(new_chat)
          self.session.commit()
          return new_chat