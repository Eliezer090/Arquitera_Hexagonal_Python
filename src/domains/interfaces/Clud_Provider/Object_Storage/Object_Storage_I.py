from abc import ABC, abstractmethod


class Object_Storage_Interface(ABC):
    @abstractmethod
    def read(self, container_name: str, object_name: str) -> str:
        pass
