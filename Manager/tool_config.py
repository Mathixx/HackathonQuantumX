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
    }
]
