# fichier des function appellé par query 
from User.db_utilitaries import RetrieveDatabase, UpdateDatabase
from RAG_product.Faiss_database import FaissDatabase
from Product.utils_db_product import Retrieve_from_db_prd
from basemistral import BaseMistral

from typing import Tuple


def get_k_purchase(user_id:int, k:int = 5)-> str:
    """recupère les k dernière purchases dans la database

    Args:
        user_id (int): 
        k (int, optional):  Defaults to 5.

    Returns:
        str
        """
    user_id = 0 #set pour la demonstration
    res = ""
    purchases = RetrieveDatabase.get_last_k_purchases_by_user_id(user_id, k )
    for purchase in purchases:
        res += RetrieveDatabase.tuple_to_detailed_text(purchase)
        res += '\n' 
    if not res:
        res = "NO HISTORY"
    return res 



def get_k_nearests_product(query: str, k :int = 3) -> str :
    """Use RAG to get the 5 nearest product from the query , based on similarity with the descriptions 

    Args:
        query (str): 
        k (int, optional): Defaults to 3.
    """
    id_produits_list = FaissDatabase.search(query, k )
    produits = Retrieve_from_db_prd.get_product_by_id_list(id_produits_list)

    
    #Appeler la fonction qui affiche les produits
    
    #on va résumer les infos, donc pour ca on appelle baseMistral
    model = BaseMistral()
    text = ''
    i=0
    for produit in produits:
        text_produit = Retrieve_from_db_prd.product_to_paragraph(produit)
        text += f"Produit {i}: \n "
        text += model.summarize(text_produit)
        text += '\n'
        
    return text



def get_k_nearest_users( user_id : int , k= 3) -> list[Tuple]:
    """ utilise faiss pour rechercher les k users les plus proches en ce basant sur le texte d'information

    Args:
        user_id (int)

    Returns:
        list[Tuple]
    """
    path_db_users = "Manager/User/userDB/user_index_faiss.faiss"
    user_id = 0 # pour le test
    
    user_info = RetrieveDatabase.get_user_info(user_id)
    
    index_neighbours = FaissDatabase.search(user_info, k, db_path= path_db_users)
    
    users = []
    for i in range(len(index_neighbours)):
        if index_neighbours[i] == user_id:
            index_neighbours.pop(i)
        else:
            users.append(RetrieveDatabase.get_user_by_id(index_neighbours[i]))
    return index_neighbours, users 


def get_best_purchases_from_neighbours(user_id = 0) -> str:
    """ Renvoie les 3 meilleurs achats des  3 voisins les plus proches, en version texte , cf function 

    Args:
        user_id (int, optional): _description_. Defaults to 0.
    """
    user_id = 0 
    index_neighbours, _  = get_k_nearest_users(user_id, 3)
    purchases =  []
    for i in index_neighbours:
        neighbours_id = index_neighbours[i]
        purchase_neighbours = RetrieveDatabase.get_best_k_purchases_by_user_id(neighbours_id, 3)
        purchases.extend(purchase_neighbours)
    text = ""
    for purchase in purchases : 
        text += RetrieveDatabase.tuple_to_detailed_text(purchase)
        text += "\n"
        
    return text 



def get_not_delivered(user_id: int) -> str:
    """renvoie un texte résumant les purchases non délivrer du user

    Args:
        user_id (int)
    """
    purchases = RetrieveDatabase.get_not_delivered_purchases(user_id)
    text = "Here are the commands not received: \n"
    
    for purchase in purchases:
        product_name, purchase_date  = purchase[2], purchase[3]
        text += f"{product_name}, purchased on the {product_name}"
        
    return text



def cancel_purchase(user_id: int,
                      purchase_id: int = None,
                      product_name: str = None,
                      purchased_date = None) -> str:
    """cancel order

    Args:
        user_id (int): 
        purchase_id (int, optional):. Defaults to None.
        product_name (str, optional): Defaults to None.
        purchased_date (_type_, optional):  Defaults to None.

    Returns:
        str: _description_
    """
    res = UpdateDatabase.suppress_purchase(user_id, purchase_id, product_name, purchased_date)
    return res 





    

    