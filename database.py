import sqlite3
import hashlib

def create_database():
    """Create the database and users table"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            otp_secret TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    create_database()
