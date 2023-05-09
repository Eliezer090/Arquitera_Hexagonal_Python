import pytest
import logging
from unittest import mock,TestCase
from src.adapters import Redis_Adapter
from src.domains import Database_Action


class TestRedisAdapter(TestCase):

    @mock.patch('redis.Redis', autospec=True)
    def test_get_key(self, redis_mock):
        # Configuração do mock
        redis_instance_mock = redis_mock.return_value
        redis_instance_mock.get.return_value = 'conteúdo_mock'
        adapter = Redis_Adapter('localhost', 6379, None)

        # Execução do teste
        resultado = adapter.getkey('minha_chave')

        # Verificações
        redis_mock.assert_called_once_with(
            host='localhost', port=6379, decode_responses=True)
        redis_instance_mock.ping.assert_called_once_with()
        redis_instance_mock.get.assert_called_once_with('minha_chave')
        assert resultado == 'conteúdo_mock'
    
    @mock.patch('redis.Redis', autospec=True)
    def test_getkey_without_key(self, redis_mock):
        redis_instance_mock = redis_mock.return_value
        redis_instance_mock.get.return_value = "value_mock"

        adapter = Redis_Adapter('localhost', 6379, None)

        with pytest.raises(ValueError) as exc_info:
            adapter.getkey('')

        assert str(exc_info.value) == "Key parameter is mandatory"

    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connected')
    @mock.patch('redis.Redis', autospec=True)
    def test_get_key_with_Exception(self,redis_mock,connected_mock):
        with self.assertLogs(level="ERROR") as log:
            connected_mock.side_effect = Exception('Error getting message Redis:')
            adapter = Redis_Adapter('localhost', 6379, None)
            adapter.getkey('minha_chave')
            assert "Error getting message Redis:" in log.output[0] 

    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connected')
    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    @mock.patch('redis.Redis', autospec=True)
    def test_getkey_connects_when_not_connected(self,redis_mock,mock_connected,mock_connect):
        adapter = Redis_Adapter('localhost', 6379, None)
        # Substitui o comportamento do método __connected para sempre retornar False
        mock_connect.return_value=False
        # Cria um mock para o atributo redis_instance
        adapter.redis_instance = mock.Mock()
        adapter.getkey('minha_chave')
        # Verifica se o método __connect foi chamado
        mock_connect.assert_called_once()

    @mock.patch('redis.Redis', autospec=True)
    def test_set_key(self, redis_mock):
        # Configuração do mock
        redis_instance_mock = redis_mock.return_value
        redis_instance_mock.set.return_value = True
        adapter = Redis_Adapter('localhost', 6379, None)

        # Execução do teste
        resultado = adapter.setKey('minha_chave', 'meu_valor')

        # Verificações
        redis_mock.assert_called_once_with(
            host='localhost', port=6379, decode_responses=True)
        redis_instance_mock.ping.assert_called_once_with()
        redis_instance_mock.set.assert_called_once_with(
            'minha_chave', 'meu_valor')
        assert resultado is True

    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    def test_setKey_raises_exception_when_key_is_none(self,mock_connect):
        adapter = Redis_Adapter('localhost', 6379, None)
        with pytest.raises(ValueError) as excinfo:
            adapter.setKey(None, 'test_content')
        assert str(excinfo.value) == "Key parameter is mandatory"

    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connected')
    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    @mock.patch('redis.Redis', autospec=True)
    def test_setKey_connects_when_not_connected(self,redis_mock,mock_connected,mock_connect):
        adapter = Redis_Adapter('localhost', 6379, None)
        # Substitui o comportamento do método __connected para sempre retornar False
        mock_connect.return_value=False
        # Cria um mock para o atributo redis_instance
        adapter.redis_instance = mock.Mock()
        adapter.setKey('test_key', 'test_content')
        # Verifica se o método __connect foi chamado
        mock_connect.assert_called_once()
    
    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    def test_setKey_logs_exception_when_set_fails(self,mock_connect):
        adapter = Redis_Adapter('localhost', 6379, Database_Action())
        adapter.redis_instance = mock.Mock()
        adapter.redis_instance.set.side_effect = Exception('test_exception')
        with self.assertLogs(level="ERROR") as mock_logging_error:
            adapter.setKey('test_key', 'test_content')
            assert "Error setting message Redis:" in mock_logging_error.output[0] 


    @mock.patch('redis.Redis', autospec=True)
    @mock.patch.object(Redis_Adapter, 'setKey')
    def test_get_key_database(self,  set_key_mock, redis_mock):
        # Configuração do mock
        redis_instance_mock = redis_mock.return_value
        redis_instance_mock.get.return_value = None
        # Cria uma implementação simulada de Database_Action que retorna um valor fixo

        class Mock_Database_Action(Database_Action):
            def getkey_DataBase(self, key: str):
                return "conteudo_da_chave"

        # Cria uma instância de Redis_Adapter com a implementação simulada de Database_Action
        mock_database_action = Mock_Database_Action()
        adapter = Redis_Adapter(
            'localhost', 6379, database_action=mock_database_action)

        # Execução do teste
        resultado = adapter.getkey_DataBase('minha_chave')

        # Verificações
        redis_mock.assert_called_once_with(
            host='localhost', port=6379, decode_responses=True)
        redis_instance_mock.ping.called
        redis_instance_mock.get.assert_called_once_with('minha_chave')
        set_key_mock.assert_called_once_with(
            'minha_chave', 'conteudo_da_chave')
        assert resultado == 'conteudo_da_chave'

    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    def test_getkey_DataBase_raises_exception_when_key_is_none(self,mock_connect):
        adapter = Redis_Adapter('localhost', 6379, None)
        with pytest.raises(ValueError) as excinfo:
            adapter.getkey_DataBase(None)
        assert str(excinfo.value) == "Key parameter is mandatory"

    @mock.patch('redis.Redis', autospec=True)
    def test_redis_connection_exception(self, redis_mock):
        # Configuração do mock
        redis_instance_mock = redis_mock.return_value
        redis_instance_mock.ping.side_effect = Exception("Failed to connect")

        # Cria uma instância de Redis_Adapter
        adapter = Redis_Adapter('localhost', 6379, None)

        # Execução do teste
        connected = adapter._Redis_Adapter__connected()

        # Verificações
        redis_mock.assert_called_once_with(
            host='localhost', port=6379, decode_responses=True)
        redis_instance_mock.ping.assert_called_once()
        assert not connected
    
    @mock.patch.object(Redis_Adapter, 'setKey')
    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connected')
    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    @mock.patch('redis.Redis', autospec=True)
    def test_getkey_DataBase_connects_when_not_connected(self,redis_mock,mock_connect,mock_connected,setkey_mock):
        adapter = Redis_Adapter('localhost', 6379, Database_Action())
        # Substitui o comportamento do método __connected para sempre retornar False
        mock_connected.return_value=False
        adapter.database_action.getkey_DataBase = mock.Mock(return_value='test_value')        
        # Cria um mock para o atributo redis_instance
        adapter.redis_instance = mock.Mock()
        adapter.getkey_DataBase('test_key')
        # Verifica se o método __connect foi chamado
        assert mock_connect.call_count == 2

    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connect')
    @mock.patch.object(Redis_Adapter, '_Redis_Adapter__connected')
    def test_getkey_DataBase_logs_exception_when_set_fails(self,mock_connected,mock_connect):
        adapter = Redis_Adapter('localhost', 6379, Database_Action())
        mock_connected.side_effect = Exception('test_exception')
        with self.assertLogs(level="ERROR") as mock_logging_error:
            adapter.getkey_DataBase('test_key')
            assert "Error getting Redis or Database message:" in mock_logging_error.output[0] 
