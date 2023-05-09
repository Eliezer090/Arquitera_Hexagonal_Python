from unittest.mock import Mock,MagicMock
import pytest
import inject
from typing import List
from pytest_mock import MockFixture

from src.domains.actions import Database_Action,Cache_Action,Object_Storage_Action,Queue_Action
from src.domains.usecases import Example_UseCase
from src.domains.entities import User


@pytest.fixture
def queue() -> MagicMock:
    # Mockando a base de dedos
    return MagicMock(spec=Queue_Action)


@pytest.fixture
def database() -> Mock:
    # Mockando a base de dedos
    return Mock(spec=Database_Action)


@pytest.fixture
def object_storage() -> Mock:
    # Mockando o object storage
    return Mock(spec=Object_Storage_Action)


@pytest.fixture
def cache() -> Mock:
    # Mockando a implementação do cache
    return Mock(spec=Cache_Action)


@pytest.fixture
def injector(database: Mock, object_storage: Mock, cache: Mock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(Queue_Action, queue)
                               .bind(Database_Action, database)
                               .bind(Object_Storage_Action, object_storage)
                               .bind(Cache_Action, cache))

@pytest.fixture
def users() -> List[User]:
    users: List[User] = []
    users.append(User(id=1, username='alice', email='alice@example.com'))
    users.append(User(id=2, username='bob', email='bob@example.com'))
    return users

class Test_Example_UseCase:
    def test_Example(self, injector: None, mocker: MockFixture, queue: Mock, database: Mock, object_storage: Mock, cache: Mock, users: List[User]):
        # Cria a instância do Example_UseCase com os mocks
        example_usecase = Example_UseCase(
            queue=queue, database=database, object_storage=object_storage, cache_action=cache)
        example_usecase.Example()
        message = mocker.MagicMock()
        channel = mocker.MagicMock()
        method = mocker.MagicMock()
        
        database.get_all_Users.return_value = users
        cache.getkey_DataBase.return_value = "chamou do banco"

        example_usecase.process_message(channel, method, None, message)
        
        assert database.get_all_Users.called
        assert cache.getkey_DataBase.called
        assert object_storage.read.called
        assert cache.setKey.called
        assert cache.getkey.called