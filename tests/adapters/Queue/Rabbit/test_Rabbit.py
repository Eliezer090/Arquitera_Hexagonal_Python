import pytest
import pika
from unittest import TestCase, mock
from src.adapters import Rabbit_Adapter
from unittest.mock import MagicMock

class TestRabbitAdapter(TestCase):

    def setUp(self):
        self.rabbit_adapter = Rabbit_Adapter('localhost', 5672, 'guest', 'guest')
        self.message_handler_mock = mock.MagicMock()
    
    def test_get_messages(self):
        with mock.patch.object(self.rabbit_adapter, '_Rabbit_Adapter__connect'):
            with mock.patch.object(self.rabbit_adapter, '_Rabbit_Adapter__receive_message') as receive_message_mock:
                self.rabbit_adapter.getMessages('test_queue', self.message_handler_mock)
                receive_message_mock.assert_called_once_with('test_queue', self.message_handler_mock)
    
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__is_connected')
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__receive_message')
    def test_get_messages_with_error(self,receive_message_mock,is_connected_mock):
        with self.assertLogs(level="ERROR") as log:
            is_connected_mock.side_effect = Exception('Error receiving message from rabbit:')
            self.rabbit_adapter.getMessages('test_queue', self.message_handler_mock)
            assert "Error receiving message from rabbit:" in log.output[0]  

    def test_get_messages_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.rabbit_adapter.getMessages('queue', 'not_callable')

    def test_get_messages_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.rabbit_adapter.getMessages(None, lambda: None)

    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__connect')
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__send_message')
    def test_post_message(self, send_message_mock, connect_mock):
        result = self.rabbit_adapter.postMessage('test_queue', 'test_message')
        send_message_mock.assert_called_once_with('test_queue', 'test_message')
        self.assertTrue(result)

    def test_post_messages_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.rabbit_adapter.postMessage(None, lambda: None)
            
    @mock.patch('pika.BlockingConnection', autospec=True)
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__send_message')
    def test_post_message_with_call_private_function__connect(self, send_message_mock,block_connection_mock):
        self.rabbit_adapter.postMessage('test_queue', 'test_message')
        assert block_connection_mock.called

    @mock.patch('pika.BlockingConnection')
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__send_message')
    def test_post_message_with_call_private_function__connect_with_exception(self, send_message_mock,mock_connection):   
        with self.assertLogs(level="ERROR") as log:
            mock_connection.side_effect = Exception('Failed to connect to rabbit')
            self.rabbit_adapter.postMessage('test_queue', 'test_message')
            assert "Failed to connect to rabbit" in log.output[0]          
    
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__is_connected')
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__receive_message')
    def test_post_messages_with_error(self,receive_message_mock,is_connected_mock):
        with self.assertLogs(level="ERROR") as log:
            is_connected_mock.side_effect = Exception('Error the send message to rabbit:')
            self.rabbit_adapter.postMessage('test_queue', 'test_message')
            assert "Error the send message to rabbit:" in log.output[0]

    def test_is_connected(self):
        assert not self.rabbit_adapter._Rabbit_Adapter__is_connected()
        self.rabbit_adapter.connection = mock.Mock()
        assert not self.rabbit_adapter._Rabbit_Adapter__is_connected()
        self.rabbit_adapter.connection.is_closed = False
        assert self.rabbit_adapter._Rabbit_Adapter__is_connected()


    def test_send_message(self):
        self.rabbit_adapter.channel = MagicMock()
        self.rabbit_adapter.channel.queue_declare = MagicMock()
        self.rabbit_adapter.channel.basic_publish = MagicMock()
        
        assert self.rabbit_adapter._Rabbit_Adapter__send_message('queue', 'message')
        self.rabbit_adapter.channel.queue_declare.assert_called_with(queue='queue')
        self.rabbit_adapter.channel.basic_publish.assert_called_with(
            exchange="", routing_key='queue', body='message')

    def test_send_message_raises_exception_when_key_is_none(self):
        with pytest.raises(ValueError) as excinfo:
            self.rabbit_adapter._Rabbit_Adapter__send_message(None, 'message')
        assert str(excinfo.value) == "Queue parameter is mandatory"

    def test_send_message_exception(self):
        self.rabbit_adapter.channel = MagicMock()
        self.rabbit_adapter.channel.queue_declare = MagicMock(side_effect=Exception('Error'))
        
        with pytest.raises(Exception):
            with self.assertLogs(level="ERROR") as log:
                assert not self.rabbit_adapter._Rabbit_Adapter__send_message('queue', 'message')
                assert "Error the send message to rabbit: Error" in log.output[0]
    
    def test_receive_message(self):
        self.rabbit_adapter.channel = MagicMock()
        self.rabbit_adapter.channel.queue_declare = MagicMock()
        self.rabbit_adapter.channel.basic_consume = MagicMock()
        self.rabbit_adapter.channel.start_consuming = MagicMock()
        
        message_handler = MagicMock()
        self.rabbit_adapter._Rabbit_Adapter__receive_message('queue', message_handler)
        self.rabbit_adapter.channel.queue_declare.assert_called_with(queue='queue')
        self.rabbit_adapter.channel.basic_consume.assert_called_once()
        self.rabbit_adapter.channel.start_consuming.assert_called_once()

    def test_receive_message_exception(self):
        self.rabbit_adapter.channel = MagicMock()
        self.rabbit_adapter.channel.queue_declare = MagicMock(side_effect=Exception('Error'))
        
        
        with self.assertLogs(level="ERROR") as log:
            message_handler = MagicMock()
            self.rabbit_adapter._Rabbit_Adapter__receive_message('queue', message_handler)
            assert "Error receiving message: Error" in log.output[0]
    
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__is_connected')
    @mock.patch.object(Rabbit_Adapter, '_Rabbit_Adapter__connect')
    def test_receive_message_function_callback(self,connect_mock,is_connected_mock):
        # Set up mock objects
        ch = MagicMock()
        method = MagicMock()
        properties = MagicMock()
        body = "test message"
        message_handler = MagicMock()     
        self.rabbit_adapter.channel = MagicMock()

        self.rabbit_adapter.getMessages("test_queue", message_handler)

        # Recupera a função que foi passada como callback do basic_consume call_args
        callback = self.rabbit_adapter.channel.basic_consume.call_args[1][
        "on_message_callback"
        ]
        # Invoca a função de callback
        callback(ch, method, properties, body)

        # verifica se afunção message_handler foi chamada com os argumentos corretos
        message_handler.assert_called_once_with(ch, method, properties, body)

    
    def test_close_connection(self):
        # Set up Rabbit_Adapter instance
        self.rabbit_adapter.connection = MagicMock()

        # Call __close_connection method
        self.rabbit_adapter._Rabbit_Adapter__close_connection()

        # Check that connection.close was called
        self.rabbit_adapter.connection.close.assert_called_once()

    def test_close_connection_exception(self):
        self.rabbit_adapter.connection = MagicMock()
        self.rabbit_adapter.connection.close.side_effect = Exception("test error")
        
        
        with self.assertLogs(level="ERROR") as log:
            self.rabbit_adapter._Rabbit_Adapter__close_connection()
            assert "Error closing connection: test error" in log.output[0]

    def tearDown(self):
        self.rabbit_adapter = None
        