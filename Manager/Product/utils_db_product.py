import sqlite3
from typing import List, Tuple , Dict
import os

class Retrieve_from_db_prd:
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
        conn = sqlite3.connect(Retrieve_from_db_prd.product_db_path)
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
        conn = sqlite3.connect(Retrieve_from_db_prd.product_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (product_id))
        product = cursor.fetchone()
        conn.close()
        return product
    
    @classmethod
    def product_to_paragraph(product):
        """
        Prend une ligne de la table 'products' sous forme de tuple et retourne un paragraphe descriptif.

        Arguments:
            product (tuple): Une ligne de la table, avec les colonnes (product_id, name, avg_ratings, no_of_ratings, actual_price, product_description).

        Retour:
            str: Un paragraphe descriptif détaillé sur le produit.
        """
        product_id, name, avg_ratings, no_of_ratings, actual_price, product_description = product

        # Construire le paragraphe
        paragraph = f"The product '{name}' is priced at ${actual_price:.2f}. "
        if avg_ratings is not None and no_of_ratings is not None:
            paragraph += f"It has an average rating of {avg_ratings:.1f} out of 5, based on {no_of_ratings} reviews. "
        elif avg_ratings is not None:
            paragraph += f"It has an average rating of {avg_ratings:.1f} out of 5. "
        else:
            paragraph += "No ratings are available for this product yet. "
        
        if product_description:
            paragraph += f"Here is a brief description: {product_description}"
        else:
            paragraph += "Unfortunately, there is no detailed description available for this product."
        
        return paragraph

