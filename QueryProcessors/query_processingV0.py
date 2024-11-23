import json
from jsonschema import validate, ValidationError
from typing import List, Dict
import sqlite3
import os

db_path = os.path.join("ProductDB", "products.db")

# JSON Schema definition
SCHEMA = {
    "type": "object",
    "properties": {
        "category_abstract": {"type": "string"},
        "category_precise": {"type": "string"},
        "max_price": {"type": ["number", "null"], "minimum": 0},
        "min_price": {"type": ["number", "null"], "minimum": 0},
        "min_rating": {"type": ["number", "null"], "minimum": 0, "maximum": 5},
        "rating_count": {"type": ["integer", "null"], "minimum": 0},
        "preference": {
            "type": "string",
            "enum": ["best_seller", "highest_rating", "cheapest", "most_popular"]
        }
    },
    "required": ["category_abstract", "category_precise", "preference"],
    "additionalProperties": False
}

# Function to validate the input JSON object
def validate_query(input_data: Dict) -> bool:
    """
    Validates the input JSON object against the predefined schema.

    Args:
        input_data (Dict): The input JSON object to validate.

    Returns:
        bool: True if the input data is valid, raises ValidationError otherwise.
    """
    try:
        validate(instance=input_data, schema=SCHEMA)
        return True
    except ValidationError as e:
        raise ValueError(f"Invalid input data: {e.message}")

# Function to query a SQLite database based on input criteria
def query_database(criteria: Dict, db_path=db_path) -> List[Dict]:
    """
    Searches the SQLite database based on the provided criteria.

    Args:
        criteria (Dict): The validated input criteria for filtering the database.
        db_path (str): Path to the SQLite database file.

    Returns:
        List[Dict]: A list of results matching the criteria.
    """
    # Extract criteria
    category_abstract = criteria["category_abstract"]
    category_precise = criteria["category_precise"]
    max_price = criteria.get("max_price")
    min_price = criteria.get("min_price")
    min_rating = criteria.get("min_rating")
    rating_count = criteria.get("rating_count")
    preference = criteria["preference"]

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Check if it successfully connected
    if not connection:
        raise ValueError("Could not connect to the database.")

    # Build the SQL query with optional filters
    query = f"""
    SELECT name, main_category, sub_category, avg_ratings, no_of_ratings, actual_price
    FROM products
    WHERE main_category = ?
      AND sub_category = ?
    """

    params = [category_abstract, category_precise]

    if min_price is not None and max_price is not None:
        query += " AND actual_price BETWEEN ? AND ?"
        params.extend([min_price, max_price])
    elif min_price is not None:
        query += " AND actual_price >= ?"
        params.append(min_price)
    elif max_price is not None:
        query += " AND actual_price <= ?"
        params.append(max_price)

    if min_rating is not None:
        query += " AND avg_ratings >= ?"
        params.append(min_rating)

    if rating_count is not None:
        query += " AND no_of_ratings >= ?"
        params.append(rating_count)

    # Execute the query
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    # Map the results to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    results_list = [dict(zip(columns, row)) for row in results]

    # Sort results based on preference
    if preference == "highest_rating":
        results_list.sort(key=lambda x: x.get("avg_ratings", 0), reverse=True)
    elif preference == "cheapest":
        results_list.sort(key=lambda x: x.get("actual_price", float("inf")))
    elif preference == "most_popular":
        results_list.sort(key=lambda x: x.get("no_of_ratings", 0), reverse=True)

    # Close the connection
    connection.close()

    return results_list

# Example usage (to be removed in production)
if __name__ == "__main__":
    # Example input JSON
    input_json = {
        "category_abstract": "electronics",
        "category_precise": "smartphones",
        "max_price": 1000.0,
        "min_price": 500.0,
        "min_rating": 4.5,
        "rating_count": 100,
        "preference": "highest_rating"
    }

    # Validate and query
    try:
        if validate_query(input_json):
            print("DB Path:", db_path)
            results = query_database(input_json, db_path)
            print("Query Results:", results)
    except ValueError as e:
        print(e)

