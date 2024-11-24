import os
import sqlite3
import faiss
import pandas as pd
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

df = pd.read_csv('Manager\\User\\Sample_Purchase_Table_Instances.csv', index_col=False)
for i in range(df.shape[0]):
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute(
            """
            INSERT INTO purchases (product_id, product_name, delivered, rating, review, buyer_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (df.iloc[i,0], df.iloc[i,1],1, df.iloc[i,3], df.iloc[i,4], df.iloc[i,5])
        )

    conn.commit()
    conn.close()