import faiss 
from mistralai import Mistral
import numpy as np
from getpass import getpass
import pickle 
import time

def get_text_embedding(input, client, i: int = 0):
    """
    Obtenir l'embedding d'un texte en utilisant le modèle Mistral.

    Args:
        input (str): Texte à transformer en embedding.
        client (Mistral): Client Mistral.

    Returns:
        list[float]: Embedding du texte.
    """
    time.sleep(0.2)
    embeddings_batch_response = client.embeddings.create(
        model="mistral-embed",
        inputs=input
    )
    return embeddings_batch_response.data[0].embedding

class FaissDatabase:
    """
    Classe pour gérer la base de données Faiss.
    """
    
    # Demander la clé API via la console
    API_KEY = 'W7jZ5RO87zVxhO0gehFjjg0TqyXasmGj'
    
    # Initialiser le client Mistral avec la clé API
    client = Mistral(api_key=API_KEY)

    # Chemins vers les fichiers de la base de données
   
    database_faiss_path = "Manager/RAG_product/index_faiss.faiss"
    
    @staticmethod
    def add_texts_to_database(texts: list[str], db_path : str = None ) -> None:
        """
        Mettre à jour la base de données en ajoutant des textes.

        Args:
            texts (list[str]): Textes à ajouter.
            db_path : path de la base de donnée si ce n'est pas celle des produits 
        """
        if db_path is None:
            db_path = FaissDatabase.database_faiss_path

        # Obtenir les embeddings des textes
        text_embeddings = np.array([get_text_embedding(texts[i], FaissDatabase.client, i ) for i in range(len(texts))])

        # Lire l'index Faiss existant
        try:
            index = faiss.read_index(db_path)
        except Exception as e:
            print(f"Erreur lors de la lecture de l'index Faiss : {e}")
            return

        # Ajouter les nouveaux embeddings à l'index
        index.add(text_embeddings)

        # Sauvegarder l'index mis à jour
        faiss.write_index(index, db_path)

        


    @staticmethod
    def create_data_base(texts: list[str], db_path : str = None ) -> None:
        """
        Créer une nouvelle base de données Faiss en ajoutant des textes.

        Args:
            texts (list[str]): Textes à ajouter.
            db_path : path de la base de donnée si ce n'est pas celle des produits 
        """
        if db_path is None:
            db_path = FaissDatabase.database_faiss_path
        texts = [text[:8000] for text in texts ]
        # Obtenir les embeddings des textes
        text_embeddings = np.array([get_text_embedding(texts[i], FaissDatabase.client, i ) for i in range(len(texts))])

        # Déterminer la dimension des embeddings
        dimension = text_embeddings.shape[1]

        # Créer un nouvel index Faiss
        index = faiss.IndexFlatL2(dimension)

        # Ajouter les embeddings à l'index
        index.add(text_embeddings)

        # Sauvegarder l'index
        faiss.write_index(index, db_path)

        

    @staticmethod
    def search(query: str, k: int = 1, db_path: str = None ) -> list[str]:
        """
        Rechercher les k plus proches voisins de la requête.

        Args:
            query (str): Texte de la requête.
            k (int, optional): Nombre de résultats à retourner. Par défaut à 1.
            db_path : lien de la base de donnée 
        Returns:
            list[int]: Liste des id des textes proches 
           
        """
        if db_path is None:
            db_path = FaissDatabase.database_faiss_path

        # Obtenir l'embedding de la requête
        query_embedding = np.array([get_text_embedding(query, FaissDatabase.client)])

        # Lire l'index Faiss
        try:
            index = faiss.read_index(db_path)
        except Exception as e:
            print(f"Erreur lors de la lecture de l'index Faiss : {e}")
            return []

        result = index.search(query_embedding, k)
        if isinstance(result, tuple) and len(result) == 2:
            D, I = result
        else:
            I = result
        
        return  I.tolist()[0]

      
      
        

    @staticmethod
    def modifie_input(text: str, index: int, db_path: str = None) -> None:
        """
        Modifie une entrée dans l'index en remplaçant le vecteur existant par l'embedding du texte donné.

        Args:
            text (str): Le texte à convertir en vecteur.
            index (int): L'indice du vecteur à modifier dans l'index.
            db_path (str, optionnel): Le chemin vers la base de données FAISS. Si non spécifié, le chemin par défaut sera utilisé.
        """
        
        if db_path is None:
            db_path = FaissDatabase.database_faiss_path

        # Étape 1: Obtenir l'embedding du texte
        text_embedding = np.array(get_text_embedding(text, FaissDatabase.client))
        
        # Étape 2: Charger l'index existant depuis le fichier
        index = faiss.read_index(db_path)

        # Étape 3: Extraire le vecteur à modifier à partir de l'index
        vector_to_modify = index.reconstruct(index)

        # Étape 4: Remplacer le vecteur existant par le nouveau vecteur (embedding du texte)
        new_vector = text_embedding  

        # Étape 5: Créer un nouvel index pour ajouter le vecteur modifié
        new_index = faiss.IndexFlatL2(vector_to_modify.shape[0])

        # Ajouter tous les vecteurs de l'index, sauf celui qui est modifié
        for i in range(index.ntotal):
            if i != index:
                new_index.add(index.reconstruct(i).reshape(1, -1))
            else:
                # Ajouter le nouveau vecteur à l'indice spécifié
                new_index.add(new_vector.reshape(1, -1))

        # Étape 6: Sauvegarder l'index modifié dans le fichier
        faiss.write_index(new_index, db_path)
