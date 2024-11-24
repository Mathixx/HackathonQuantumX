# fichier des function appellé par query 
from User.db_utilitaries import RetrieveDatabase
from RAG_product.Faiss_database import FaissDatabase
from Product.utils_db_product import Retrieve_from_db_prd
from basemistral import BaseMistral
def get_k_purchase(user_id:int, k:int = 5)-> str:
    """recupère les k derniière purchases dans la database

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
        
    
    
    
     
    