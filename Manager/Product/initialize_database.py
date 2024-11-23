import sqlite3

def initialize_database(db_path: str):
    # Connect to SQLite database (creates it if it doesn't exist)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create the `products` table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        name TEXT,
        main_category TEXT,
        sub_category TEXT,
        avg_ratings REAL,
        no_of_ratings INTEGER,
        actual_price REAL
    )
    """)

    # Insert sample data
    sample_data = [
        ("iPhone 14", "electronics", "smartphones", 4.8, 2500, 999.99),
        ("Samsung Galaxy S22", "electronics", "smartphones", 4.6, 1800, 799.99),
        ("OnePlus 10", "electronics", "smartphones", 4.5, 1200, 699.99),
        ("MacBook Air", "electronics", "laptops", 4.9, 3200, 1249.99),
        ("Dell XPS 13", "electronics", "laptops", 4.7, 2100, 1149.99),
        ("Sony WH-1000XM5", "electronics", "headphones", 4.8, 1500, 399.99)
    ]
    cursor.executemany("""
    INSERT INTO products (name, main_category, sub_category, avg_ratings, no_of_ratings, actual_price)
    VALUES (?, ?, ?, ?, ?, ?)
    """, sample_data)

    # Commit changes and close the connection
    connection.commit()
    connection.close()
    print(f"Database initialized and populated with sample data at '{db_path}'.")

if __name__ == "__main__":
    initialize_database("ProductDB/products.db")
