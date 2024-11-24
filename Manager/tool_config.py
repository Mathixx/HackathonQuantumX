# tool_config.py

tools_conf = [
    {
        "type": "function",
        "function": {
            "name": "get_k_nearests_product",
            "description": "Search for the k products in the seller database that are closest to the user's needs. This function is to be used when looking for products to suggest to the client. If this information is already available, it should not be called.",
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
            "name": "no_more_action_needed",
            "description": "Indicates that no more actio or information is needed for the current task. This should be called whenever the query is empty but also when the asked task has already been accomplished.",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "Adds to the cart the list of products the client explicitly wants to buy. This should be called whenever the client wants to add products to the cart.",
            "parameters": {
                "type": "object",
                "properties": {
                    "precise_product_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "The names of the products to add to the cart."
                    },
                    "prices": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "description": "The prices of the products to add to the cart."
                    },
                    "amounts": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "description": "The quantity of each product to add to the cart."
                    }
                },
                "required": ["precise_product_names", "prices", "amounts"],
                "additionalProperties": False
            }
        }
    }
]


