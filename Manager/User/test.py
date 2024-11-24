from db_utilitaries import RetrieveDatabase


print(RetrieveDatabase.get_last_k_purchases_by_user_id(1, k=3))