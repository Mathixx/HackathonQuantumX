# fichier des function appellé par query 
from User.db_utilitaries import RetrieveDatabase


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
    
    