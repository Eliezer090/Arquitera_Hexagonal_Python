import pytest
import inject
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from src.domains.interfaces import Example_Interface
from src.domains.actions import Example_action


@pytest.fixture
def example() -> MagicMock:
    return MagicMock(spec=Example_Interface)


@pytest.fixture
def injector(example: MagicMock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(Example_Interface, example))


class Test_Example_action:
    def test_execute(self, injector: None, mocker: MockFixture, example: MagicMock):
        Example_action().execute()
        assert example.Example.called
