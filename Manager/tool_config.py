# tool_config.py

tools_conf = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_best_products",
            "description": "Gets the best products based on user preferences and the database of products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category_abstract": {
                        "type": "string",
                        "description": "The abstract category of the product (e.g., electronics, fashion, etc.)."
                    },
                    "category_precise": {
                        "type": "string",
                        "description": "The specific subcategory of the product (e.g., smartphones, laptops)."
                    },
                    "max_price": {
                        "type": ["number", "null"],
                        "minimum": 0,
                        "description": "The maximum price for filtering products. Null if not applicable."
                    },
                    "min_price": {
                        "type": ["number", "null"],
                        "minimum": 0,
                        "description": "The minimum price for filtering products. Null if not applicable."
                    },
                    "min_rating": {
                        "type": ["number", "null"],
                        "minimum": 0,
                        "maximum": 5,
                        "description": "The minimum average rating required for the product. Null if not applicable."
                    },
                    "rating_count": {
                        "type": ["integer", "null"],
                        "minimum": 0,
                        "description": "The minimum number of ratings required for the product. Null if not applicable."
                    },
                    "preference": {
                        "type": "string",
                        "enum": ["best_seller", "highest_rating", "cheapest", "most_popular"],
                        "description": "The user's preference for sorting the results."
                    }
                },
                "required": ["category_abstract", "category_precise", "preference"],
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
                        "type": "int",
                        "description": "The unique identifier for the user whose purchase history is being analyzed."
                    },
                    "k": {
                        "type": "int",
                        "description": "How many purchases to recover"
                    },
                 
                },
                "required": ["user_id", "include_current_orders"],
                "additionalProperties": False
            }
        }
    }
]
