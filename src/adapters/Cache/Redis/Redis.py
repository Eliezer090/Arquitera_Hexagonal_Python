import redis
import inject
import logging
from ....domains.interfaces import Cache_Interface
from ....domains.actions import Database_Action


class Redis_Adapter(Cache_Interface): 
    @inject.params()
    def __init__(self, host: str, port: int, database_action: Database_Action):
        self.host = host
        self.port = port
        self.database_action = database_action
        self.__connect()

    def __connected(self) -> bool:
        '''
            Check if redis is connected
        '''
        try:
            self.redis_instance.ping()
            return True
        except:
            return False

    def __connect(self):
        '''
           Connect to redis
        '''
        self.redis_instance = redis.Redis(
            host=self.host, port=self.port, decode_responses=True)

    def getkey(self, key: str) -> str:
        '''
            Get the value of a Redis key
        '''
        if not key:
            raise ValueError("Key parameter is mandatory")
        try:
            if not self.__connected():
                self.__connect()
            return self.redis_instance.get(key)
        except Exception as e:
            logging.error(
                f"Error getting message Redis: {str(e)}", stack_info=True)

    def setKey(self, key: str, content: str) -> bool:
        '''
            Set value to a Redis key
        '''
        if not key:
                raise ValueError("Key parameter is mandatory")
        try:            
            if not self.__connected():
                self.__connect()
            return self.redis_instance.set(key, content)
        except Exception as e:
            logging.error(
                f"Error setting message Redis: {str(e)}", stack_info=True)

    def getkey_DataBase(self, key: str) -> str:
        '''
            Get value from a Redis key, if you don't find the value in redis, search the database!
        '''
        if not key:
                raise ValueError("Key parameter is mandatory")
        try:
            value_key = None
            
            if not self.__connected():
                self.__connect()
                
            if self.__connected():
                value_key = self.redis_instance.get(key)

            if value_key == None:
                value_key = self.database_action.getkey_DataBase(key)
                self.setKey(key, value_key)

            return value_key
        except Exception as e:
            logging.error(
                f"Error getting Redis or Database message: {str(e)}", stack_info=True)
