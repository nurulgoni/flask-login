import pytest
from unittest.mock import patch, MagicMock
from app.app import app  # Adjust the import if necessary

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def mock_cursor(fetchone_return_value=None):
    # Create a mock cursor
    mock_cursor = MagicMock()
    mock_cursor.execute = MagicMock()
    mock_cursor.fetchone.return_value = fetchone_return_value
    return mock_cursor

@patch('app.app.mysql')
def test_login_success(mock_mysql, client):
    mock_cursor_instance = mock_cursor({'id': 1, 'username': 'testuser'})
    mock_mysql.connection.cursor.return_value = mock_cursor_instance

    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Hi testuser!!' in response.data
    assert b'Welcome to the index page...' in response.data

@patch('app.app.mysql')
def test_login_failure(mock_mysql, client):
    mock_cursor_instance = mock_cursor(None)
    mock_mysql.connection.cursor.return_value = mock_cursor_instance

    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b'Incorrect username / password!' in response.data

@patch('app.app.mysql')
def test_register_success(mock_mysql, client):
    mock_cursor_instance = mock_cursor()
    mock_mysql.connection.cursor.return_value = mock_cursor_instance

    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 200
    assert b'You have successfully registered!' in response.data

@patch('app.app.mysql')
def test_register_failure(mock_mysql, client):
    mock_cursor_instance = mock_cursor({'id': 1, 'username': 'existinguser'})
    mock_mysql.connection.cursor.return_value = mock_cursor_instance

    response = client.post('/register', data={
        'username': 'existinguser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 200
    assert b'Account already exists!' in response.data
