import sqlite3
import os 
import pandas as pd

import sys
from pathlib import Path

# Ajouter le dossier parent au chemin Python
sys.path.append(str(Path(__file__).resolve().parent.parent))

from RAG_product.Faiss_database import FaissDatabase 

class InitializeDatabase:
    
    data_path = "Manager\\Product\\data_cosmetic.csv"
    db_path = "Manager\\Product\\products.db"
    
    def __init__(self):
        """Initialise la base de donnée et la remplie avec les données du csv 
        """
        df = pd.read_csv(InitializeDatabase.data_path)
        df.dropna(axis = 0)
        df = df[df["product_description"].apply(lambda x: isinstance(x, str))]
        print(df.head())
        connection = sqlite3.connect(InitializeDatabase.db_path)
        cursor = connection.cursor()
        
         # Create the `products` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL,
            avg_ratings REAL NOT  NULL,
            no_of_ratings INTEGER,
            actual_price REAL, 
            product_description TEXT
        )
        """)
        products = []
        texts = []
        for i in range(df.shape[0]):
            #Récupération des données 
            name = df.iloc[i,1]
            print(type(name))
            avg_rating = df.iloc[i,2]
            no_of_ratings = df.iloc[i,3]
            price = df.iloc[i,4]
            #création de la description 
            print(type(df.iloc[i,5]))
            description = name + ': \n' + df.iloc[i,5]
            
            #ajout des produits à la listes des textes pour le RAG
            texts.append(description)
            products.append((name, avg_rating, no_of_ratings, price, description))
            
            
        cursor.executemany("""
            INSERT INTO products (name, avg_ratings, no_of_ratings, actual_price, product_description)
            VALUES (?, ?, ?, ?, ?)
            """, 
            products)
        #création de la database faiss
        FaissDatabase.create_data_base(texts)
            
        connection.commit()
        connection.close() 
        print(f"Database initialized and populated with sample data at '{InitializeDatabase.db_path}'.")
           



if __name__ == "__main__":
    
    InitializeDatabase()