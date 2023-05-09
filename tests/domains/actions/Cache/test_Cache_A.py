import pytest
import inject
from typing import List
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from src.domains.interfaces import Cache_Interface
from src.domains.actions import Cache_Action


@pytest.fixture
def cache_interface_Mock() -> MagicMock:
    return MagicMock(spec=Cache_Interface)


@pytest.fixture
def injector(cache_interface_Mock: MagicMock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(Cache_Interface, cache_interface_Mock))


class Test_Cache_Action:
    def test_getkey(self, injector: None, cache_interface_Mock: MagicMock):
        value_get = 'Value 123'
        cache_interface_Mock.getkey.return_value = value_get
        return_get = Cache_Action().getkey('test')
        assert return_get == value_get

    def test_setKey(self, injector: None, mocker: MockFixture, cache_interface_Mock: MagicMock):
        assert Cache_Action().setKey('test', 'Value key test')

    def test_getkey_DataBase(self, injector: None, mocker: MockFixture, cache_interface_Mock: MagicMock):
        value_get_db = 'Value 123'
        cache_interface_Mock.getkey_DataBase.return_value = value_get_db
        return_get = Cache_Action().getkey_DataBase('test')
        assert return_get == value_get_db
