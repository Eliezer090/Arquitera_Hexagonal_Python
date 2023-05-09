import inject
import os
import logging
from flask import Flask
from .domains.interfaces import Example_Interface, QueueInterface, DatabaseInterface, Object_Storage_Interface, Cache_Interface
from .domains.usecases import Example_UseCase
from .domains.actions import Queue_Action, Database_Action, Object_Storage_Action, Cache_Action
from .adapters import Rabbit_Adapter, SQLite_Adapter, Bucket_Provider_Adapter, Redis_Adapter


def configure_inject(app: Flask) -> None:

    def config(binder: inject.Binder) -> None:
        # Environment variables RABBIT
        rabbit_host = os.environ.get('RABBIT_HOST', '')
        rabbit_port = os.environ.get('RABBIT_PORT', 999)
        rabbit_user = os.environ.get('RABBIT_USER', '')
        rabbit_password = os.environ.get('RABBIT_PASSWORD', '')

        # Environment variables SQLITE
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'sample.db')
        SQLite_host = os.environ.get('SQLITE_HOST', f'sqlite:///{db_path}')

        # Environment variables REDIS
        redis_host = os.environ.get('REDIS_HOST', '')
        redis_port = os.environ.get('REDIS_PORT', 999)

        # Environment Level de Log
        level_log = os.environ.get('LEVEL_LOG', 'ERROR')

        # Environment name the service
        name_service = os.environ.get('NAME_SERVICE', 'EXAMPLE_SERVICE')

        logging.basicConfig(level=level_log.upper(
        ), format='%(asctime)s - '+name_service+' - %(levelname)s - %(message)s')

        binder.bind(Example_Interface,
                    Example_UseCase(Queue_Action(), Database_Action(), Object_Storage_Action(), Cache_Action()))
        binder.bind(QueueInterface, Rabbit_Adapter(
            rabbit_host, rabbit_port, rabbit_user, rabbit_password))
        binder.bind(DatabaseInterface, SQLite_Adapter(SQLite_host))
        binder.bind(Object_Storage_Interface, Bucket_Provider_Adapter())
        binder.bind(Cache_Interface, Redis_Adapter(
            redis_host, redis_port, Database_Action()))

    inject.configure(config)
