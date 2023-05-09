
import inject
from ...interfaces import QueueInterface


class Queue_Action:

    @inject.autoparams()
    def getMessages(self, queue: str, message_handler, Queue_Interface: QueueInterface):
        Queue_Interface.getMessages(queue, message_handler)

    @inject.autoparams()
    def postMessage(self, queue: str, message: str, Queue_Interface: QueueInterface) -> bool:
        return Queue_Interface.postMessage(queue, message)
