from abc import ABC, abstractmethod


class Cache_Interface(ABC):
    @abstractmethod
    def getkey(self, key: str) -> str:
        pass

    @abstractmethod
    def setKey(self, key: str, content:str) -> bool:
        pass

    @abstractmethod
    def getkey_DataBase(self, key: str) -> str:
        pass
