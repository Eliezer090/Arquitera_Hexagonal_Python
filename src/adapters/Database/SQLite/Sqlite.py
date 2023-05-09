from typing import List
from ....domains.interfaces import DatabaseInterface
from sqlalchemy.orm import Session
from ....domains.entities import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class SQLite_Adapter(DatabaseInterface):
    def __init__(self, UrlConnection: str):
        self.engine = create_engine(UrlConnection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_all_Usersdb(self) -> List[User]:
        return self.session.query(User).all()
    
    def getkey_DataBase(self, key:str) -> str:
        return 'valor da chave '+key
