# functions.py

from User.db_utilitaries import RetrieveDatabase, UpdateDatabase
from RAG_product.Faiss_database import FaissDatabase
from Product.utils_db_product import Retrieve_from_db_prd
from basemistral import BaseMistral
from typing import Tuple

def no_more_action_needed() -> str:
    """Indicates no more information is needed."""
    return [], "The task has been accomplished. No more action and information is needed."


def user_purchase_history(user_id=0, k: int = 5) -> str:
    """Retrieve the k latest purchases in the database."""
    res = ""
    user_id = 0
    purchases = RetrieveDatabase.get_last_k_purchases_by_user_id(user_id, k)
    for purchase in purchases:
        product_id = purchase[1]
        price = Retrieve_from_db_prd.get_product_by_id(product_id)[-2]
        res += RetrieveDatabase.tuple_to_detailed_text(purchase)
        res += '\n'
        res += f'The user payed {price} euros for this product'
    if not res:
        res = "NO HISTORY"
    return [], res


def get_k_nearests_product(query: str, k: int = 3) -> Tuple[str, list]:
    """Retrieve the k nearest products based on the query."""
    id_produits_list = FaissDatabase.search(query, k)
    produits = Retrieve_from_db_prd.get_product_by_id_list(id_produits_list)
    products_refined = [(produit[1], produit[2], produit[4]) for produit in produits]

    # Use BaseMistral for summarization
    model = BaseMistral()
    text = ''
    i = 0
    for produit in produits:
        text_produit = Retrieve_from_db_prd.product_to_paragraph(produit)
        text += f"Produit {i}: \n"
        text += model.summarize(text_produit)
        text += '\n'
        i += 1

    return products_refined, text

def add_purchase(product_id: int, product_name: str, user_id: int) -> Tuple[str, list]:
    """add purchase to the database

    Args:
        user_id (int): 
        product_name (str): 
        quantity (int): 

    Returns:
        str: 
    """
    user_id = 0 
    res = UpdateDatabase.add_purchase(product_id, product_name, user_id, delivered = 0, rating=None, review=None)
    _ = []
    return res,_





def collect_user_feedback(user_id:int, purchase_id:int, rating:int, review:str) -> Tuple[str, list]:
    """collect user feedback

    Args:
        user_id (int): 
        product_id (int): 
        rating (int): 
        review (str): 

    Returns:
        str: 
    """
    res = UpdateDatabase.update_review(user_id, purchase_id, rating, review)
    _ = []
    return res,_

def get_total_spent(user_id:int) -> Tuple[str, list]:
    """get total spent by user

    Args:
        user_id (int): 

    Returns:
        str: 
        
    """
    purchases = RetrieveDatabase.get_all_purchases(user_id)
    products_ids = [purchase[1] for purchase in purchases]
    total_spent = 0
    for product_id in products_ids:
        product = Retrieve_from_db_prd.get_product_by_id(product_id)
        total_spent += product[-2]
        
    _ = []
    return f"The user has spent a total of ${total_spent:.2f} on the platform.", _

def add_to_cart(precise_product_names: list[str], prices: list[int], amounts: list[int]):
    """
    Returns a list of the products added to the cart.
    """
    return [(product, amount, price) for product, amount, price in zip(precise_product_names, amounts, prices)], "Liste of products added to the cart."


names_to_functions= {
    "get_k_nearests_product": get_k_nearests_product,
    "user_purchase_history": user_purchase_history,
    "no_more_action_needed": no_more_action_needed,
    "add_to_cart": add_to_cart
}