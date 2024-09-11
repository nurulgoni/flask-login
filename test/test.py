import unittest
from unittest.mock import patch, MagicMock
from app.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        # Setup Flask testing client
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Patch MySQL connection
        self.patcher = patch('flask_mysqldb.MySQL.connection', autospec=True)
        self.mock_connection = self.patcher.start()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    def tearDown(self):
        self.patcher.stop()
        self.app_context.pop()

    def test_login_post_invalid(self):
        # Setup mock to simulate failed login
        self.mock_cursor.fetchone.return_value = None

        response = self.client.post('/login', data=dict(username='wrong', password='wrong'))
        self.assertIn(b'Incorrect username / password!', response.data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Mock login and simulate logout
        self.client.post('/login', data=dict(username='valid_user', password='valid_password'))
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_register_post_invalid(self):
        # Setup mock to simulate registration
        self.mock_cursor.fetchone.return_value = None

        response = self.client.post('/register', data=dict(username='new_user', password='password', email='invalid'))
        self.assertIn(b'Invalid email address!', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
