import sqlite3
import hashlib
import datetime

def create_connection():
    connection = sqlite3.connect("app_data.db")
    return connection

def create_users_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            full_name TEXT,
            password TEXT,
            photo_path TEXT
        )
    """)

    connection.commit()
    connection.close()

def seed_default_user():
    if not username_exists("admin"):
        add_user("admin", "Admin", "Admin123!")

def username_exists(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    connection.close()
    return result is not None

def add_user(username, full_name, password):
    connection = create_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, full_name, password) VALUES (?, ?, ?)",
        (username, full_name, hashed_password)
    )

    connection.commit()
    connection.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_stored_password(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None
    return result[0]

def get_full_name(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT full_name FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None
    return result[0]

def create_posts_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_post(username, content):
    connection = create_connection()
    cursor = connection.cursor()

    timestamp = datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p")

    cursor.execute(
        "INSERT INTO posts (username, content, created_at) VALUES (?, ?, ?)",
        (username, content, timestamp)
    )

    connection.commit()
    connection.close()


def get_posts_by_user(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT content, created_at FROM posts WHERE username = ? ORDER BY id DESC",
        (username,)
    )
    results = cursor.fetchall()

    connection.close()
    return results

def update_password(username, new_password):
    connection = create_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(new_password)

    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))

    connection.commit()
    connection.close()

def update_photo_path(username, path):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET photo_path = ? WHERE username = ?", (path, username))
    connection.commit()
    connection.close()


def get_photo_path(username):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT photo_path FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None