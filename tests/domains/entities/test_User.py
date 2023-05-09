from src.domains import User

def test_user_creation():
    user = User(username='testuser', email='testuser@example.com', id=11)
    assert user.id == 11
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'