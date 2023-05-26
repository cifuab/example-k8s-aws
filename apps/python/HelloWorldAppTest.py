import unittest
import sqlite3
from fastapi.testclient import TestClient
from HelloWorldApp import app
from db import create_tables,save_user


class HelloWorldAppTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000"
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        create_tables(self.cursor)

        # Start the FastAPI application
        self.client = TestClient(app)

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_save_user(self):
        url = f"{self.base_url}/hello/john"
        data = {"date_of_birth": "1990-01-01"}
        response = self.client.put(url,json=data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{"message": "User saved/updated successfully."})

        # Check if the user is saved in the database
        self.cursor.execute("SELECT * FROM users WHERE username = ?",("john",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1],"john")
        self.assertEqual(result[2],"1990-01-01")

    def test_get_user_birthday_today(self):
        # Save a user with the birthday today
        save_user(self.cursor,"john","2000-05-23")

        url = f"{self.base_url}/hello/john"
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{"message": "Hello, john! Happy birthday!"})

    def test_get_user_birthday_in_future(self):
        # Save a user with the birthday in the future
        save_user(self.cursor,"jane","2000-06-10")

        url = f"{self.base_url}/hello/jane"
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{"message": "Hello, jane! Your birthday is in 18 day(s)"})

    def test_get_user_not_found(self):
        url = f"{self.base_url}/hello/unknown"
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{"message": "User not found."})


if __name__ == "__main__":
    unittest.main()
