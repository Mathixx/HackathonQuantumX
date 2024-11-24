# tool_config.py

tools_conf = [
    {
        "type": "function",
        "function": {
            "name": "get_k_nearests_product",
            "description": "Search for the k products closest to the user's query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query string to search for similar products."
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
            "name": "get_k_nearest_users",
            "description": "Search for users who have a similar profile to the target user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique identifier for the user."
                    },
                    "k": {
                        "type": "integer",
                        "description": "The number of nearest users to retrieve.",
                        "default": 3
                    }
                },
                "required": ["user_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_best_purchases_from_neighbours",
            "description": "Retrieve the best products purchased by users with similar profiles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique identifier for the user.",
                        "default": 0
                    }
                },
                "required": ["user_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_not_delivered",
            "description": "Returns a text summarizing the undelivered purchases of the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique identifier for the user."
                    }
                },
                "required": ["user_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_insufficient_info",
            "description": "Handles cases where there is not enough information to proceed with a product search and requests additional details from the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "missing_fields": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "The list of fields that are missing or insufficient for the search."
                        },
                        "description": "The specific fields that are missing from the input, requiring user input."
                    },
                    "suggested_fields": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "The list of fields that the system suggests the user to provide next."
                        },
                        "description": "Fields that are most critical to gather additional information for a search."
                    },
                    "action": {
                        "type": "string",
                        "enum": ["request_info", "abort"],
                        "description": "Action to be taken: request more information or abort the process."
                    }
                },
                "required": ["missing_fields", "action"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_user_purchase_history",
            "description": "Analyzes user purchase history and current orders to identify relevant patterns or preferences for product recommendations.",
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
            "name": "add_purchase",
            "description": "Add a new purchase to the database for a given user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "The unique identifier for the product."
                    },
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product being purchased."
                    },
                    "user_id": {
                        "type": "integer",
                        "description": "The unique identifier for the user"
                    }
                },
                "required": ["user_id", "product_name", "quantity"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_purchase",
            "description": "Cancels a purchase based on the provided parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique identifier for the user."
                    },
                    "purchase_id": {
                        "type": "integer",
                        "description": "The unique identifier for the purchase.",
                        
                    },
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product.",
                        
                    },
                    "purchased_date": {
                        "type": "string",
                        "description": "The date of the purchase.",
                        
                    }
                },
                "required": ["user_id"],
                "additionalProperties": False
            }
        }
    },
    
]
