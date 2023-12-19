# database_operations.py
import sqlite3

def initialize_database():
    # Create and connect to a SQLite database
    conn = sqlite3.connect('telegram_users.db')
    cursor = conn.cursor()

    # Create a table if not exists to store user information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            chat_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

def save_user_info(user_id, username, first_name, last_name, chat_id):
    conn = sqlite3.connect('telegram_users.db')
    cursor = conn.cursor()

    # Check if the user already exists in the database
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        # Save user information to the database if it's a new user
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, chat_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, chat_id))
        conn.commit()
    else:
        # If the user already exists, you can choose to update their information or ignore
        print(f"User {user_id} already exists in the database.")

    conn.close()
