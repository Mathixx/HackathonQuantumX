import os
import sqlite3

# Define the userDB folder
USER_DB_FOLDER = "userDB"
USER_DB_FILE = "user_data.db"

# Ensure the userDB folder exists
os.makedirs(USER_DB_FOLDER, exist_ok=True)

# Define the path to the database
user_db_path = os.path.join(USER_DB_FOLDER, USER_DB_FILE)

# Initialize the database
conn = sqlite3.connect(user_db_path)
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    purchase_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER,
    review TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS preferences (
    preference_id INTEGER PRIMARY KEY,
    preference_key TEXT NOT NULL,
    preference_value TEXT NOT NULL
);
""")

# Commit and close connection
conn.commit()
conn.close()

print(f"Database initialized at {user_db_path}")

