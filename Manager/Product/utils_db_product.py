import sqlite3
from typing import List, Tuple , Dict
import os

class Retrieve_from_db:
     # Define the productDB folder and file
    PRODUCT_DB_FOLDER = "Manager\\Product"
    PRODUCT_DB_FILE = "products.db"

    # Define the path to the database
    product_db_path = os.path.join(PRODUCT_DB_FOLDER, PRODUCT_DB_FILE)
    
    
    @classmethod
    def get_product_by_id_list( product_id_list : list[int] ) -> list[Tuple]:
        """ récupère tous les produuits d'une liste d'id 

        Args:
            product_id_list (list[int])

        Returns:
            list[Tuple]
        """
        # Connexion à la base de données
        conn = sqlite3.connect(Retrieve_from_db.product_db_path)
        cursor = conn.cursor()

        

        # Créer une chaîne de paramètres pour la requête SQL
        placeholders = ', '.join(['?'] * len(product_id_list))

        # Requête SQL avec des paramètres
        query = f"SELECT * FROM purchases WHERE purchase_id IN ({placeholders})"

        # Exécuter la requête
        cursor.execute(query, product_id_list)
        results = cursor.fetchall()

        # Fermer la connexion
        conn.close()
        return results
    
    @staticmethod
    def get_product_by_id(product_id:int) -> Tuple :
        """Retrieve a specific product by ID from the database."

        Args:
            product_id (int): 

        Returns:
            Tuple
        """
        conn = sqlite3.connect(Retrieve_from_db.product_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (product_id))
        product = cursor.fetchone()
        conn.close()
        return product

