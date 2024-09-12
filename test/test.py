import unittest
from unittest.mock import patch, MagicMock
from app.app import app  # Adjust the import if necessary

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def mock_cursor(self, fetchone_return_value=None):
        # Create a mock cursor
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        mock_cursor.fetchone.return_value = fetchone_return_value
        return mock_cursor

    @patch('app.app.mysql')
    def test_login_success(self, mock_mysql):
        mock_cursor = self.mock_cursor({'id': 1, 'username': 'testuser'})
        mock_mysql.connection.cursor.return_value = mock_cursor

        response = self.app.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hi testuser!!', response.data)

    @patch('app.app.mysql')
    def test_login_failure(self, mock_mysql):
        mock_cursor = self.mock_cursor(None)
        mock_mysql.connection.cursor.return_value = mock_cursor

        response = self.app.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username / password!', response.data)

    @patch('app.app.mysql')
    def test_register_success(self, mock_mysql):
        mock_cursor = self.mock_cursor()
        mock_mysql.connection.cursor.return_value = mock_cursor

        response = self.app.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully registered!', response.data)

    @patch('app.app.mysql')
    def test_register_failure(self, mock_mysql):
        mock_cursor = self.mock_cursor({'id': 1, 'username': 'existinguser'})
        mock_mysql.connection.cursor.return_value = mock_cursor

        response = self.app.post('/register', data={
            'username': 'existinguser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account already exists!', response.data)

if __name__ == '__main__':
    unittest.main()
