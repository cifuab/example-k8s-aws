import sqlite3
import pytest
from fastapi.testclient import TestClient

from hello_world import app

client = TestClient(app)


def test_client():
    return TestClient(app)


def setup_teardown():
    # Set up a test database and tables
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, dateOfBirth TEXT)")
    cursor.execute("INSERT INTO users (username, dateOfBirth) VALUES ('Alice', '1990-01-01')")
    cursor.execute("INSERT INTO users (username, dateOfBirth) VALUES ('Bob', '1985-05-10')")
    cursor.execute("INSERT INTO users (username, dateOfBirth) VALUES ('Charlie', '1995-11-15')")
    connection.commit()
    yield
    # Tear down the test database and tables
    cursor.execute("DROP TABLE users")
    connection.commit()
    connection.close()


def test_get_existing_user(test_client):
    response = test_client.get("/hello/Alice")
    assert response.status_code == 200
    assert response.json() == {'username': 'Alice','dateOfBirth': '1990-01-01'}


def test_get_non_existing_user(test_client):
    response = test_client.get("/hello/Eve")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_create_user(test_client):
    response = test_client.put("/hello/Dave",json={"dateOfBirth": "1982-03-25"})
    assert response.status_code == 201
    assert response.json() == {'username': 'Dave','dateOfBirth': '1982-03-25'}


def test_update_user(test_client):
    response = test_client.post("/hello/Bob",json={"dateOfBirth": "1990-08-20"})
    assert response.status_code == 200
    assert response.json() == {'username': 'Bob','dateOfBirth': '1990-08-20'}


def test_update_non_existing_user(test_client):
    response = test_client.post("/hello/Eve",json={"dateOfBirth": "1999-12-31"})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_get_all_users(test_client):
    response = test_client.get("/hello")
    assert response.status_code == 200
    assert response.json() == [
        {'username': 'Alice','dateOfBirth': '1990-01-01'},
        {'username': 'Bob','dateOfBirth': '1985-05-10'},
        {'username': 'Charlie','dateOfBirth': '1995-11-15'}
    ]


def test_create_user_missing_date_of_birth(test_client):
    response = test_client.put("/hello/Eve",json={})
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['body','dateOfBirth'],'msg': 'field required','type': 'value_error.missing'}]}


def test_update_user_missing_date_of_birth(test_client):
    response = test_client.post("/hello/Alice",json={})
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['body','dateOfBirth'],'msg': 'field required','type': 'value_error.missing'}]}
