import pytest
from src.adapters.Database import SQLite_Adapter
from src.domains.entities import User

@pytest.fixture
def adapter():
    adapter = SQLite_Adapter('sqlite:///:memory:')
    User.metadata.create_all(adapter.engine)    
    return adapter

@pytest.fixture
def adapter_with_users(adapter):
    user1 = User(username='Alice', email='alice@example.com')
    user2 = User(username='Bob', email='bob@example.com')
    adapter.session.add(user1)
    adapter.session.add(user2)
    adapter.session.commit()
    return adapter

def test_get_all_Usersdb(adapter_with_users):
    users = adapter_with_users.get_all_Usersdb()
    assert isinstance(users, list)
    assert len(users) == 2
    assert all(isinstance(user, User) for user in users)

def test_getkey_DataBase(adapter):
    key = 'test_key'
    result = adapter.getkey_DataBase(key)
    assert result == 'valor da chave ' + key