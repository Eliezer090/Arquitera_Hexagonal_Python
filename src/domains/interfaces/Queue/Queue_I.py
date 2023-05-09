from abc import ABC, abstractmethod


class QueueInterface(ABC):
    @abstractmethod
    def getMessages(self, queue: str, message_handler) -> None:
        print(queue)
        pass

    @abstractmethod
    def postMessage(self, queue: str, message: str) -> bool:
        pass
