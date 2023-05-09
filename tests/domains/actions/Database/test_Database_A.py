import pytest
import inject
from typing import List
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from src.domains.interfaces import DatabaseInterface
from src.domains.actions import Database_Action
from src.domains.entities import User


@pytest.fixture
def database_interface_Mock() -> MagicMock:
    return MagicMock(spec=DatabaseInterface)


@pytest.fixture
def injector(database_interface_Mock: MagicMock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(DatabaseInterface, database_interface_Mock))


@pytest.fixture
def users() -> List[User]:
    users: List[User] = []
    users.append(User(id=1, username='alice', email='alice@example.com'))
    users.append(User(id=2, username='bob', email='bob@example.com'))
    return users


class Test_Database_Action:
    def test_get_all_Users(self, injector: None, mocker: MockFixture, database_interface_Mock: MagicMock, users: List[User]):
        database_interface_Mock.get_all_Usersdb.return_value = users
        users_DB: List[User] = Database_Action().get_all_Users()
        assert users_DB == users

    def test_getkey_DataBase(self, injector: None, mocker: MockFixture, database_interface_Mock: MagicMock):
        value_key_db = 'Value key db'
        database_interface_Mock.getkey_DataBase.return_value = value_key_db
        value_return_db: str = Database_Action().getkey_DataBase('key')
        assert value_return_db == value_key_db

    def test_get_all_Users_and_getkey_DataBase_with_exception(self):
        # Cria uma implementação simulada de DatabaseInterface que lança uma exceção
        class MockDatabaseInterface(DatabaseInterface):
            def get_all_Usersdb(self):
                raise Exception("Database error")

            def getkey_DataBase(self, key: str):
                raise Exception("Get Key DataBase error")

        # Cria uma instância de Database_Action com a implementação simulada de DatabaseInterface
        data_base_interface = MockDatabaseInterface()
        database_action = Database_Action()

        # Verifica se o método get_all_Users lança uma exceção com a mensagem de erro esperada
        with pytest.raises(SystemError, match="Error search all users: Database error"):
            database_action.get_all_Users(data_base_interface)
        
        # Verifica se o método getkey_DataBase lança uma exceção com a mensagem de erro esperada
        with pytest.raises(SystemError, match="Error get key database: Get Key DataBase error"):
            database_action.getkey_DataBase('key',data_base_interface)
    