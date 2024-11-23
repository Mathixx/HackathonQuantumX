import os
import sqlite3

# Define the userDB folder
USER_DB_FOLDER = "userDB"
USER_DB_FILE = "user_data.db"

# Define the path to the database
user_db_path = os.path.join(USER_DB_FOLDER, USER_DB_FILE)

def add_purchase(product_name, rating=None, review=None):
    """Add a new purchase to the database."""
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO purchases (product_name, rating, review)
        VALUES (?, ?, ?)
        """,
        (product_name, rating, review)
    )
    conn.commit()
    conn.close()
    print(f"Added purchase: {product_name}")

def update_review(purchase_id, rating=None, review=None):
    """Update the rating or review of an existing purchase."""
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    if rating is not None and review is not None:
        cursor.execute(
            """
            UPDATE purchases
            SET rating = ?, review = ?
            WHERE purchase_id = ?
            """,
            (rating, review, purchase_id)
        )
    elif rating is not None:
        cursor.execute(
            """
            UPDATE purchases
            SET rating = ?
            WHERE purchase_id = ?
            """,
            (rating, purchase_id)
        )
    elif review is not None:
        cursor.execute(
            """
            UPDATE purchases
            SET review = ?
            WHERE purchase_id = ?
            """,
            (review, purchase_id)
        )
    conn.commit()
    conn.close()
    print(f"Updated purchase ID {purchase_id} with rating: {rating}, review: {review}")
