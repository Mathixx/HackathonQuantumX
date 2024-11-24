# functions.py

from User.db_utilitaries import RetrieveDatabase, UpdateDatabase
from RAG_product.Faiss_database import FaissDatabase
from Product.utils_db_product import Retrieve_from_db_prd
from basemistral import BaseMistral
from typing import Tuple



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


def get_best_purchases_from_neighbours(user_id = 0) -> Tuple[str, Tuple]:
    """ Renvoie les 3 meilleurs achats des  3 voisins les plus proches, en version texte , cf function 
        Renvoie aussi les produits associers 

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
    products_id = []
    for purchase in purchases : 
        products_id.append( purchase[1])
        text += RetrieveDatabase.tuple_to_detailed_text(purchase)
        text += "\n"
    products = Retrieve_from_db_prd.get_product_by_id_list(products_id)
    
    products_refined =[ (product[1],product[2], product[4]) for product in products]
    return  products_refined, text