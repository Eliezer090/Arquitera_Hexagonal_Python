import pytest
import inject
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from src.domains.interfaces import QueueInterface
from src.domains.actions import Queue_Action


@pytest.fixture
def queue() -> MagicMock:
    return MagicMock(spec=QueueInterface)


@pytest.fixture
def injector(queue: MagicMock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(QueueInterface, queue))


class Test_Queue_Action:
    def test_getMessages(self, injector: None, mocker: MockFixture, queue: MagicMock):
        # Cria o objeto Queue_Action
        queue_action = Queue_Action()

        # Cria um mock para o manipulador de mensagem
        message_handler = mocker.MagicMock()

        # Chama o método getMessages
        queue_action.getMessages(queue='nome_da_fila',
                                 message_handler=message_handler)
        assert queue.getMessages.called

    def test_postMessage(self, injector: None, mocker: MockFixture, queue: MagicMock):
        # Cria o objeto Queue_Action
        queue_action = Queue_Action()

        # Cria um mock para o manipulador de mensagem
        message_handler = mocker.MagicMock()

        # Chama o método postMessage
        queue_action.postMessage(queue='nome_da_fila', message='mensagem')
        assert queue.postMessage.called
