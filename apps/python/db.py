import sqlite3


def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        date_of_birth TEXT
                    )''')


def save_user(cursor,username,date_of_birth):
    cursor.execute('''INSERT OR REPLACE INTO users (username, date_of_birth)
                      VALUES (?, ?)''',(username,date_of_birth))


def get_user(cursor,username):
    cursor.execute('''SELECT date_of_birth FROM users WHERE username = ?''',(username,))
    row = cursor.fetchone()

    if row:
        return User(username,row[0])


class User:
    def __init__(self,username,date_of_birth):
        self.username = username
        self.date_of_birth = date_of_birth
