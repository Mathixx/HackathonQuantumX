import os
import sqlite3
import datetime
import sys
import pandas as pd
from typing import List, Tuple , Dict
from pathlib import Path
# Ajouter le dossier parent au chemin Python
sys.path.append(str(Path(__file__).resolve().parent.parent))
from RAG_product.Faiss_database import FaissDatabase



class InvalidInputError(Exception):
    """Exception levée pour les entrées invalides"""
    pass


def verifier_entrees(*args):
    """Vérifie que toutes les entrées ne sont pas nulles ou vides"""
    for arg in args:
        if arg is None or (isinstance(arg, str) and not arg.strip()):
            raise InvalidInputError(f"Entrée invalide : {arg}")


class UpdateDatabase:
    """
    Class for updating the database
    """
    # Define the userDB folder
    USER_DB_FOLDER = "Manager\\User\\userDB"
    USER_DB_FILE = "user_data.db"
    USER_FAISS_DB_FILE = "user_index_faiss.faiss"
    # Ensure the userDB folder exists
    os.makedirs(USER_DB_FOLDER, exist_ok=True)

    # Define the path to the database
    user_db_path = os.path.join(USER_DB_FOLDER, USER_DB_FILE)
    user_faiss_db_path = os.path.join(USER_DB_FOLDER, USER_FAISS_DB_FILE)

    @staticmethod
    def add_purchase(product_id , product_name,  buyer_id ,delivered = 0, rating=None, review=None):
        """Add a new purchase to the database."""
        conn = sqlite3.connect(UpdateDatabase.user_db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO purchases (product_id, product_name, delivered, rating, review, buyer_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (product_id, product_name,delivered, rating, review, buyer_id)
        )
        conn.commit()
        conn.close()
        print(f"Added purchase: {product_name}")

    @staticmethod
    def update_review(purchase_id, rating=None, review=None):
        """Update the rating or review of an existing purchase."""
        conn = sqlite3.connect(UpdateDatabase.user_db_path)
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

    @staticmethod
    def add_user(first_name: str, last_name: str, age: int, gender: str = 'undifined', date_sign_in=None) -> None:
        """Add a user to the database. The first 3 args must not be empty.
        
        Args:
            first_name (str)
            last_name (str)
            age (int)
            gender (str, optional): Defaults to 'undifined'.
            date_sign_in (str, optional): Defaults to None.
        """
        if date_sign_in is None:
            date_sign_in = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            verifier_entrees(first_name, last_name, age)
        except InvalidInputError as e:
            print(f"Erreur : {e}")
            sys.exit(1)  # Arrêter le programme avec un code de sortie d'erreur
        
        conn = sqlite3.connect(UpdateDatabase.user_db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (user_first_name, user_last_name, date_sign_in, age, gender)
            VALUES (?, ?, ?, ?, ?)
            """,
            (first_name, last_name, date_sign_in, age, gender)
        )
        conn.commit()
        conn.close()
        print(f"Added user: {first_name} {last_name}")
        
    @staticmethod
    def add_users_from_df(df: pd.DataFrame)->None :
        """add multiple users from a dataframe, add their personnal_info in the faiss dataframe  

        Args:
            df (pd.DataFrame): _description_
        """
        conn = sqlite3.connect(UpdateDatabase.user_db_path)
        df.to_sql('users', conn, if_exists='append', index=False)
        conn.close()
        users_info= df['user_info'].to_list()
        FaissDatabase.add_texts_to_database(users_info, db_path= UpdateDatabase.user_faiss_db_path)

    @staticmethod
    def update_user_info(user_id: int, user_info: str)-> None :
        """Update the user information
        
        Args:
            user_id (int)
            user_info (str): If None, the program does nothing
        """
        try:
            verifier_entrees(user_id)
        except InvalidInputError as e:
            print(f"Erreur : {e}")
            sys.exit(1)  # Arrêter le programme avec un code de sortie d'erreur
        
        if user_info is not None:
            conn = sqlite3.connect(UpdateDatabase.user_db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users
                SET user_info = ?
                WHERE user_id = ?
                """,
                (user_info, user_id)
            )
            conn.commit()
            conn.close()
            print(f"Updated user ID {user_id} with personal_info: {user_info}")
            FaissDatabase.modifie_input(user_info, user_id, db_path = UpdateDatabase.user_faiss_db_path
                                        )

    @staticmethod
    def update_user_profile(user_id: int,
                            new_first_name :str =None, 
                            new_last_name: str =None,
                            new_date_sign_in: str=None,
                            new_age: int =None)-> None :
        """Update the profile of a user
        
        Args:
            user_id (int)
            new_first_name (str, optional)
            new_last_name (str, optional)
            new_date_sign_in (str, optional)
            new_age (int, optional)
        """
        try:
            verifier_entrees(user_id)
        except InvalidInputError as e:
            print(f"Erreur : {e}")
            sys.exit(1)  # Arrêter le programme avec un code de sortie d'erreur
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(UpdateDatabase.user_db_path)
            cursor = conn.cursor()

            # Création de la requête de mise à jour
            query = "UPDATE users SET "
            parameters = []
            
            if new_first_name:
                query += "user_first_name = ?, "
                parameters.append(new_first_name)
            if new_last_name:
                query += "user_last_name = ?, "
                parameters.append(new_last_name)
            if new_date_sign_in:
                query += "date_sign_in = ?, "
                parameters.append(new_date_sign_in)
            if new_age:
                query += "age = ?, "
                parameters.append(new_age)
            
            # Retirer la dernière virgule et espace
            query = query.rstrip(', ')
            query += " WHERE user_id = ?"
            parameters.append(user_id)

            # Exécution de la requête
            cursor.execute(query, parameters)
            conn.commit()

            print("Profil utilisateur mis à jour avec succès.")
        
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour du profil utilisateur : {e}")
        
        finally:
            # Fermeture de la connexion à la base de données
            if conn:
                conn.close()
                


class RetrieveDatabase:
    """
    Class for retrieving data from the database
    """
     # Define the userDB folder and file
    USER_DB_FOLDER = "Manager\\User\\userDB"
    USER_DB_FILE = "user_data.db"

    # Define the path to the database
    user_db_path = os.path.join(USER_DB_FOLDER, USER_DB_FILE)

    @staticmethod
    def get_all_users()->List[Tuple]:
        """Retrieve all users of the database

        Returns:
            List[Tuple]: list of users 
        """
        conn = sqlite3.connect(RetrieveDatabase.user_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users

    @staticmethod
    def get_all_purchases()-> List[Tuple]:
        """Retrieve all purchases from the database."""        
        conn = sqlite3.connect(RetrieveDatabase.user_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM purchases")
        purchases = cursor.fetchall()
        conn.close()
        return purchases

    @staticmethod
    def get_user_by_id(user_id:int) -> Tuple :
        """Retrieve a specific user by ID from the database."

        Args:
            user_id (int): 

        Returns:
            Tuple
        """
        conn = sqlite3.connect(RetrieveDatabase.user_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def get_purchases_by_user_id(user_id):
        """Retrieve all purchases for a specific user by user ID from the database."""
        conn = sqlite3.connect(RetrieveDatabase.user_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM purchases WHERE buyer_id = ?", (user_id,))
        purchases = cursor.fetchall()
        conn.close()
        return purchases
    
    @staticmethod
    def get_user_info(user_id: int ) -> str:
        """ retrieve user information

        Args:
            user_id (int): _description_

        Returns:
            str: user _info
        """
        try:
            verifier_entrees(user_id)
        except InvalidInputError as e:
            print(f"Erreur : {e}")
            sys.exit(1)  # Arrêter le programme avec un code de sortie d'erreur
        user = RetrieveDatabase.get_user_by_id(user_id)
        if user[-1] is None:
            return "User information is empty"
        else:
            if isinstance(user[-1] , str ):
                return user[-1]
            else :
                return "User information is empty"
            
    @staticmethod      
    def get_last_k_purchases_by_user_id(user_id:int, k: int ) -> List[Tuple ]: 
        """
        Retrieve the lasts k purchase of an user_id 

        Args:
            user_id (int)
            k:int 

        Returns:
            List[Tuple]
        """
        
        
        
        conn = sqlite3.connect(RetrieveDatabase.user_db_path) 
        cursor = conn.cursor() 
        cursor.execute( """ SELECT * 
                       FROM purchases 
                       WHERE buyer_id = ? ORDER BY purchase_id 
                       DESC LIMIT ? 
                       """, 
                       (user_id,k) ) 
        purchases = cursor.fetchall() 
        conn.close() 
        return purchases
    
    @staticmethod      
    def get_best_k_purchases_by_user_id(user_id:int, k: int ) -> List[Tuple ]: 
        """
        Retrieve the best k purchases of an user_id 

        Args:
            user_id (int)
            k:int 

        Returns:
            List[Tuple]
        """
        
        
        
        conn = sqlite3.connect(RetrieveDatabase.user_db_path) 
        cursor = conn.cursor() 
        cursor.execute( """ SELECT * 
                       FROM purchases 
                       WHERE buyer_id = ? ORDER BY rating 
                       DESC LIMIT ? 
                       """, 
                       (user_id,k) ) 
        purchases = cursor.fetchall() 
        conn.close() 
        return purchases
    
    
    @staticmethod
    def purchase_to_dict(purchase_tuple: Tuple) -> dict:
        """
        Convert a purchase tuple to a dictionary with column names.

        Args:
            purchase_tuple (tuple): A tuple representing a purchase.

        Returns:
            dict: A dictionary with column names as keys and tuple values as values.
        """
        columns = ["purchase_id",'product_id', "product_name", "delivered","rating", "review", "buyer_id"]
        purchase_dict = dict(zip(columns, purchase_tuple))
        return purchase_dict
    
    
    @staticmethod
    def user_tuple_to_dict(user_tuple: Tuple)-> dict:
        """
        Convert a user tuple to a dictionary with column names.

        Args:
            user_tuple (tuple): A tuple representing a user.

        Returns:
            dict: A dictionary with column names as keys and tuple values as values.
        """
        columns = ["user_id", "user_first_name", "user_last_name", "date_sign_in", "age", "personal_info"]
        user_dict = dict(zip(columns, user_tuple))
        return user_dict

    @staticmethod
    def tuple_to_detailed_text(purchase:Tuple ):
        """ Genere un petit texte partir d'un purchase 

        Args:
            purchase (Tuple) 

        """
        purchase_id, product_id , product_name, purchase_date,delivered_status, rating, review, buyer_id = purchase
        
        # Construire le texte descriptif
        text = f"Buyer {buyer_id} purchased the product '{product_name}' on {purchase_date}.\n"
        if delivered_status  == 0 :
            text+= " It has not been yet delivered"
        if rating is not None:
            text += f"They rated it {rating} out of 5.\n"
        else:
            text += "They did not provide a rating for this purchase.\n"
        
        if review is not None and review:
            text += f"Their review of the product is as follows: \"{review}\".\n"
        else:
            text += "They did not leave a review for this purchase.\n"
        
        return text
            
        
    
    @staticmethod
    def get_not_delivered_purchases(user_id :int ) -> list[Tuple]:
        """
        Retrieve all the purchases that as not be delivered

        Args:
            user_id (int)
            k:int 

        Returns:
            List[Tuple]
        """
        conn = sqlite3.connect(RetrieveDatabase.user_db_path) 
        cursor = conn.cursor() 
        cursor.execute( """ SELECT * 
                       FROM purchases 
                       WHERE buyer_id = ? AND 
                       delivered = 0  
                       """, 
                       (user_id) ) 
        purchases = cursor.fetchall() 
        conn.close() 
        return purchases