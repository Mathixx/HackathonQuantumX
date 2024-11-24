# functions.py

from User.db_utilitaries import RetrieveDatabase, UpdateDatabase
from RAG_product.Faiss_database import FaissDatabase
from Product.utils_db_product import Retrieve_from_db_prd
from basemistral import BaseMistral
from typing import Tuple

def no_more_info_needed() -> str:
    """Indicates no more information is needed."""
    return [], "STOP"


def user_purchase_history(user_id: int, k: int = 5) -> str:
    """Retrieve the k latest purchases in the database."""
    res = ""
    purchases = RetrieveDatabase.get_last_k_purchases_by_user_id(user_id, k)
    for purchase in purchases:
        res += RetrieveDatabase.tuple_to_detailed_text(purchase)
        res += '\n'
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




names_to_functions= {
    "get_k_nearests_product": get_k_nearests_product,
    "user_purchase_history": user_purchase_history,
    "no_more_info_needed": no_more_info_needed
}