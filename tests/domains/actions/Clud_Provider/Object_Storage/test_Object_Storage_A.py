import pytest
import inject
from typing import List
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from src.domains.interfaces import Object_Storage_Interface
from src.domains.actions import Object_Storage_Action


@pytest.fixture
def object_otorage_interface_Mock() -> MagicMock:
    return MagicMock(spec=Object_Storage_Interface)


@pytest.fixture
def injector(object_otorage_interface_Mock: MagicMock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(Object_Storage_Interface, object_otorage_interface_Mock))


class Test_Object_Storage_Action:
    def test_read(self, injector: None, mocker: MockFixture, object_otorage_interface_Mock: MagicMock):
        value_read: str = '<XML></XML>'
        object_otorage_interface_Mock.read.return_value = value_read
        return_read: str = Object_Storage_Action().read('container', 'object.xml')
        assert return_read == value_read

    def test_read_Object_Storage_with_exception(self):
        # Cria uma implementação simulada de Object_Storage_Interface que lança uma exceção
        class Mock_Object_Storage_Interface(Object_Storage_Interface):
            def read(self, container_name: str, object_name: str) -> str:
                raise Exception("Error Read cloud")

        # Cria uma instância de object_storage_action com a implementação simulada de Object_Storage_Interface
        object_storage_interface = Mock_Object_Storage_Interface()
        object_storage_action = Object_Storage_Action()

        # Verifica se o método read lança uma exceção com a mensagem de erro esperada
        with pytest.raises(SystemError, match="Error read cloud storage: Error Read cloud"):
            object_storage_action.read('container', 'object.xml', object_storage_interface)
        
