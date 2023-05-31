import sqlite3


def create_table():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                dateOfBirth TEXT
            );
            """
        )
        conn.commit()


def create_user(username: str,date_of_birth: str):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users (username, dateOfBirth) VALUES (?, ?)",
            (username,date_of_birth),
        )
        conn.commit()
        return True
    return False


def get_user(username: str):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT username, dateOfBirth FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()

    if result:
        columns = ('username', 'dateOfBirth')
        return dict(zip(columns, result))
    else:
        return None

create_table()
