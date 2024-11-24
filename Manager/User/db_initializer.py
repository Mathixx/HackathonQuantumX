import os
import sqlite3
import faiss
# Define the userDB folder
USER_DB_FOLDER = "Manager/User/userDB"
USER_DB_FILE = "user_data.db"
USER_FAISS_DB_FILE = "user_index_faiss.faiss"
# Ensure the userDB folder exists
os.makedirs(USER_DB_FOLDER, exist_ok=True)

# Define the path to the database
user_db_path = os.path.join(USER_DB_FOLDER, USER_DB_FILE)
user_faiss_db_path = os.path.join(USER_DB_FOLDER, USER_FAISS_DB_FILE)
# Initialize the database
conn = sqlite3.connect(user_db_path)
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    purchase_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    product_name TEXT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    delivered INTEGER NOT NULL,
    rating INTEGER,
    review TEXT,
    buyer_id INTEGER,
    FOREIGN KEY(buyer_id) REFERENCES users(user_id)
    
);
""")

cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_first_name TEXT NOT NULL,
    user_last_name TEXT NOT NULL,
    date_sign_in TEXT NOT NULL,
    user_age INTEGER NOT NULL,
    user_gender TEXT NOT NULL,
    user_info TEXT DEFAULT NULL
    );
    ''')



# Commit and close connection
conn.commit()
conn.close()

print(f"Database initialized at {user_db_path}")

index_users = faiss.IndexFlatL2(1024)
faiss.write_index(index_users, user_faiss_db_path)

