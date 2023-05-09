from abc import ABC, abstractmethod
from typing import List

from ...entities import User


class DatabaseInterface(ABC):

    @abstractmethod
    def get_all_Usersdb(self) -> List[User]:
        pass

    @abstractmethod
    def getkey_DataBase(self, key: str) -> str:
        pass
