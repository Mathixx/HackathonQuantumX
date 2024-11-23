import faiss 
from mistralai import Mistral
import numpy as np
from getpass import getpass
import pickle 

def get_text_embedding(input, client):
    """
    Obtenir l'embedding d'un texte en utilisant le modèle Mistral.

    Args:
        input (str): Texte à transformer en embedding.
        client (Mistral): Client Mistral.

    Returns:
        list[float]: Embedding du texte.
    """
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
    API_KEY = getpass("Entrez votre clé API Mistral : ")
    
    # Initialiser le client Mistral avec la clé API
    client = Mistral(api_key=API_KEY)

    # Chemins vers les fichiers de la base de données
    database_text_path = "texts_products_database.pkl"
    database_faiss_path = "index_faiss.faiss"
    
    @staticmethod
    def add_texts_to_database(texts: list[str]) -> None:
        """
        Mettre à jour la base de données en ajoutant des textes.

        Args:
            texts (list[str]): Textes à ajouter.
        """
        db_path = FaissDatabase.database_faiss_path

        # Obtenir les embeddings des textes
        text_embeddings = np.array([get_text_embedding(text, FaissDatabase.client) for text in texts])

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

        # Lire la liste existante de textes
        try:
            with open(FaissDatabase.database_text_path, 'rb') as file:
                text_list = pickle.load(file)
        except FileNotFoundError:
            text_list = []

        # Ajouter les nouveaux textes à la liste existante
        text_list.extend(texts)

        # Sauvegarder la liste mise à jour de textes
        with open(FaissDatabase.database_text_path, 'wb') as file:
            pickle.dump(text_list, file)

    @staticmethod
    def create_data_base(texts: list[str]) -> None:
        """
        Créer une nouvelle base de données Faiss en ajoutant des textes.

        Args:
            texts (list[str]): Textes à ajouter.
        """
        db_path = FaissDatabase.database_faiss_path

        # Obtenir les embeddings des textes
        text_embeddings = np.array([get_text_embedding(text, FaissDatabase.client) for text in texts])

        # Déterminer la dimension des embeddings
        dimension = text_embeddings.shape[1]

        # Créer un nouvel index Faiss
        index = faiss.IndexFlatL2(dimension)

        # Ajouter les embeddings à l'index
        index.add(text_embeddings)

        # Sauvegarder l'index
        faiss.write_index(index, db_path)

        # Sauvegarder la liste des embeddings dans un fichier pickle
        with open(FaissDatabase.database_text_path, 'wb') as file:
            pickle.dump(texts, file)

    @staticmethod
    def search(query: str, k: int = 1) -> list[str]:
        """
        Rechercher les k plus proches voisins de la requête.

        Args:
            query (str): Texte de la requête.
            k (int, optional): Nombre de résultats à retourner. Par défaut à 1.

        Returns:
            list[str]: Liste des textes trouvés.
        """
        db_path = FaissDatabase.database_faiss_path

        # Obtenir l'embedding de la requête
        query_embedding = np.array([get_text_embedding(query, FaissDatabase.client)])

        # Lire l'index Faiss
        try:
            index = faiss.read_index(db_path)
        except Exception as e:
            print(f"Erreur lors de la lecture de l'index Faiss : {e}")
            return []

        # Rechercher les k plus proches voisins
        D, I = index.search(query_embedding, k)

        # Lire la liste des textes existants
        try:
            with open(FaissDatabase.database_text_path, 'rb') as file:
                text_list = pickle.load(file)
        except FileNotFoundError:
            return []

        # Récupérer les textes correspondants aux indices trouvés
        res = [text_list[i] for i in I.tolist()[0]]

        return res

        




   
