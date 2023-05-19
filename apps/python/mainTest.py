import unittest
import json
from datetime import datetime, timedelta
from main import app, conn

class HelloTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.username = 'John'
        self.dob = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        self.invalid_dob = '2023-13-32'

        # Create a test table for users
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, dob DATE)')
        conn.commit()

    def tearDown(self):
        # Drop the test table after the test case
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS users')
        conn.commit()

    def test_save_user_data(self):
        response = self.client.put(f'/hello/{self.username}', json={'dateOfBirth': self.dob})
        self.assertEqual(response.status_code, 204)

        # Check if the user data is saved correctly in the database
        cur = conn.cursor()
        cur.execute('SELECT dob FROM users WHERE username = %s', (self.username,))
        result = cur.fetchone()
        self.assertIsNotNone(result)
        saved_dob = result[0].strftime('%Y-%m-%d')
        self.assertEqual(saved_dob, self.dob)

    def test_save_user_data_invalid_username(self):
        invalid_username = 'John123'
        response = self.client.put(f'/hello/{invalid_username}', json={'dateOfBirth': self.dob})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Invalid username')

    def test_save_user_data_invalid_date_of_birth(self):
        response = self.client.put(f'/hello/{self.username}', json={'dateOfBirth': self.invalid_dob})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Invalid date of birth')

    def test_save_user_data_future_date_of_birth(self):
        future_dob = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        response = self.client.put(f'/hello/{self.username}', json={'dateOfBirth': future_dob})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Date of birth must be before today')

    def test_get_hello_message(self):
        # Save user data in the database
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, dob) VALUES (%s, %s)', (self.username, self.dob))
        conn.commit()

        response = self.client.get(f'/hello/{self.username}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], f'Hello, {self.username}! Your birthday is in 5 day(s)')

    def test_get_hello_message_birthday_today(self):
        today_dob = datetime.now().strftime('%Y-%m-%d')

        # Save user data in the database
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, dob) VALUES (%s, %s)', (self.username, today_dob))
        conn.commit()

        response = self.client.get(f'/hello/{self.username}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response
