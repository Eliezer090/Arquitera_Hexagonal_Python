import time
import logging
from ...interfaces import Example_Interface
from ...actions import Queue_Action, Database_Action, Object_Storage_Action, Cache_Action
from ...entities.User import User
from typing import List


class Example_UseCase(Example_Interface):
    def __init__(self, queue: Queue_Action, database=Database_Action, object_storage=Object_Storage_Action, cache_action=Cache_Action):
        self.queue = queue
        self.database = database
        self.object_storage = object_storage
        self.cache_action = cache_action

    def Example(self):
        self.queue.getMessages('messages', self.process_message)

    def process_message(self, channel, method, properties, body):

        print(f'processado a mensagem - {body} ')
        # Pega os usuários da base sqlite - 'sample.db'

        users: List[User] = self.database.get_all_Users()
        for usr in users:
            print(f'{usr.id} | {usr.username} | {usr.email}')
        logging.info("Iniciando a busca no bucket")
        start_time = time.time()
        # Pegando xml do bucket microsservico - GCP
        print(self.object_storage.read('microsservico',
              '41171116750494000242570020000115731000000202-procCTe.xml'))
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info("Processamento concluído para a solicitação busca no bucket em %s segundos", elapsed_time)
        # Setando chave no redis
        print(self.cache_action.setKey('teste', 'Chave de teste!!!!'))
        # Pegando valor da chave do redis
        print(self.cache_action.getkey('teste'))

        # Realiza o Ack na mensagem do rabbit
        channel.basic_ack(delivery_tag=method.delivery_tag)

        print(self.cache_action.getkey_DataBase('testebanco'))
