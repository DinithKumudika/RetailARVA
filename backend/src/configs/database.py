from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class Database:
    def __init__(self, database_url) -> None:
        self._DATABASE_URL = database_url
        self._session : Session | None = None
        self._engine = None

    def connect(self):
        self._engine = create_engine(self._DATABASE_URL, connect_args={'check_same_thread': False})
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        self._session = Session()

    def get_session(self):
        return self._session

    def get_engine(self):
        return self._engine