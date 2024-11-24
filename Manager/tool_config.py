# tool_config.py

tools_conf = [
    {
        "type": "function",
        "function": {
            "name": "get_k_nearests_product",
            "description": "Search for the k products closest to the user's needs. This function is to be used when looking for products to suggest to the client. If this information is already available, it should not be called.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Description of the products to look for."
                    },
                    "k": {
                        "type": "integer",
                        "description": "The number of nearest products to retrieve.",
                        "default": 3
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "user_purchase_history",
            "description": "Retrieves the list of purchases made by the user. This should be called whenever the user asks for his previous purchases, or we need to look at his  purchases to recommend new products. Else , it should not be called.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique identifier for the user whose purchase history is being analyzed."
                    },
                    "k": {
                        "type": "integer",
                        "description": "How many purchases to recover."
                    }
                },
                "required": ["user_id", "k"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "no_more_info_needed",
            "description": "Indicates that no more information is needed for the current task. This should be called whenever the query is empty",
            "parameters": {}
        }
    }
]


