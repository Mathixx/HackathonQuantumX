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

cursor.execute(
            """
            INSERT INTO purchases (product_id, product_name, delivered, rating, review, buyer_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (0,"colourpop Lippie Pencil",1,4.5, "great buy", 0)
        )

conn.commit()
conn.close()