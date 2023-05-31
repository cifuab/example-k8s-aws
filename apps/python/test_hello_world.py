import unittest
from fastapi.testclient import TestClient
from hello_world import app, calculate_days_to_birthday

client = TestClient(app)


class HelloWorldAppTest(unittest.TestCase):
    def test_create_user(self):
        response = client.put("/hello/Dave",json={"dateOfBirth": "1982-03-25"})
        self.assertEqual(response.status_code,204)

    def test_get_existing_user(self):
        response = client.get("/hello/Dave")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{"message": "Hello, Dave! Your birthday is in {} day(s).".format(calculate_days_to_birthday('1982-03-25'))})

    def test_update_user(self):
        response = client.put("/hello/Dave",json={"dateOfBirth": "1990-08-20"})
        self.assertEqual(response.status_code,204)

    def test_get_non_existing_user(self):
        response = client.get("/hello/Eve")
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{'detail': 'User not found.'})

    def test_create_user_missing_date_of_birth(self):
        response = client.put("/hello/Eve",json={})
        self.assertEqual(response.status_code,422)
        self.assertEqual(response.json(),{
            "detail": [{"loc": ["body","dateOfBirth"],"msg": "field required","type": "value_error.missing"}]})

    def test_update_user_missing_date_of_birth(self):
        response = client.put("/hello/Alice",json={})
        self.assertEqual(response.status_code,422)
        self.assertEqual(response.json(),{
            "detail": [{"loc": ["body","dateOfBirth"],"msg": "field required","type": "value_error.missing"}]})


if __name__ == "__main__":
    unittest.main()
