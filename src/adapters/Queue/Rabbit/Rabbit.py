import pika
import threading
import typing
import logging
from ....domains.interfaces import QueueInterface


class Rabbit_Adapter(QueueInterface):
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.connection = None
        self.channel = None

    def getMessages(self, queue: str, message_handler: typing.Callable) -> None:
        '''
            Get messages the queue!
            Recived: 
                queue - queue to get messages
                message_handler - method executed after having each message
        '''
        if not callable(message_handler):
                raise TypeError(
                    "Necessary implemention the message_handler must be a callable function")

        if not queue:
            raise ValueError("Queue parameter is mandatory")
        
        try:
            
            if not self.__is_connected():
                self.__connect()
            thread = threading.Thread(
                target=self.__receive_message, args=(queue, message_handler))
            thread.start()
        except Exception as e:
            logging.error(
                f"Error receiving message from rabbit: {str(e)} ", stack_info=True)

    def postMessage(self, queue: str, message: str) -> bool:
        '''
            Send messages the rabbit
        '''
        if not queue:
            raise ValueError("Queue parameter is mandatory")
        try:
            

            if not self.__is_connected():
                self.__connect()
            return self.__send_message(queue, message)
        
        except Exception as e:  
            logging.error(
                f"Error the send message to rabbit: {str(e)} ", stack_info=True)

    def __connect(self) -> None:
        '''
            Connect with the rabbit
        '''
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                self.host, self.port, "/", credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
        except Exception as e:
            logging.error(
                f"Failed to connect to rabbit: {str(e)} ", stack_info=True)

    def __is_connected(self) -> bool:
        """
            Returns True if the RabbitMQ connection is established, otherwise False.
        """
        if self.connection and not self.connection.is_closed:
            return True
        return False

    def __send_message(self, queue: str, message: str) -> bool:
        '''
            Send messages the rabbit
        '''
        if not queue:
            raise ValueError("Queue parameter is mandatory")
        try:
            self.channel.queue_declare(queue=queue)
            self.channel.basic_publish(
                exchange="", routing_key=queue, body=message)
            return True
        except Exception as e:
            logging.error(
                f"Error the send message to rabbbit: {str(e)} ", stack_info=True)
            return False

    def __receive_message(self, queue, message_handler) -> None:
        '''
            Connect the rabbit consume messages the queue and return message in the method "process_message"
            Recived: 
                queue - queue to get messages
                message_handler - method executed after having each message
        '''
        try:
            def callback(ch, method, properties, body):
                message_handler(ch, method, properties, body)

            self.channel.queue_declare(queue=queue)
            self.channel.basic_consume(
                queue=queue, on_message_callback=callback, auto_ack=False)
            self.channel.start_consuming()
        except Exception as e:
            logging.error(
                f"Error receiving message: {str(e)} ", stack_info=True)

    def __close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            logging.error(
                f"Error closing connection: {str(e)} ", stack_info=True)
    