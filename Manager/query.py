import os
from mistralai import Mistral

### IMPORTE NECESSARY FUNCTIONS CALLED IN THE QUERY FUNCTION
# from .... import retrieve_best_productsV0
# from .... import retrieve_best_productsV1

# Retrieve the API key from the environment variable
api_key = "W7jZ5RO87zVxhO0gehFjjg0TqyXasmGj"
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")


# Define the custom agent ID TO CHANGE
custom_agent_id ="mistral-small-latest" #ag:68495cb5:20241123:expert-tpmc:bbd4e63b"

class Query:
    def __init__(self):
        """
        Initialize the Query class with a specific agent ID and client.
        """
        self.agent_id = custom_agent_id
        self.client = Mistral(api_key=api_key)
        self.tools = [
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


    def process_query(self, expert_query):
        """
        Get skincare advice based on the user's query.

        :param user_query: A string containing the user's question or concern about skincare.
        :return: A string indicating the kind of function used and an object with the result of the called function
        """
        messages = [
            {
                "role": "user",
                "content": expert_query
            }
        ]
        client = Mistral(api_key=api_key)


        try:
            # Send the query to the custom agent*
            print(messages)

            response = self.client.chat.complete(
                model = self.agent_id,
                messages = messages,
                tools = self.tools,
                tool_choice = "any",
                )
            
            print("got here 1")
            print(response.choices[0].message.tool_calls[0].function.name)
            
            if response and response.choices:
                function_name = response.choices[0].message.tool_calls[0].function.name
                parameters = response.choices[0].message.tool_calls[0].function.arguments

                print("got here 2")
                
                # Log or handle tool call details
                print(f"Function called: {function_name}")
                print(f"Parameters: {parameters}")

                # Simulate function execution for demo purposes
                if function_name == "retrieve_best_products":
                    # Normally, you'd call the actual function here
                    best_products = fake_retrieve_best_products(parameters)
                    return function_name, best_products
                else:
                    return "error", f"Unknown function: {function_name}"
            else:
                return "error", "I'm sorry, I couldn't generate a response. Please try again."
        except Exception as e:
            print("Error happens in query")
            return "error", f"An error occurred: {e}"
        
        
        
def fake_retrieve_best_products(parameters):
    return [
        {
            "name": "Product 1",
            "category": "Electronics",
            "price": 499.99,
            "rating": 4.5,
            "ratings_count": 100
        },
        {
            "name": "Product 2",
            "category": "Electronics",
            "price": 399.99,
            "rating": 4.0,
            "ratings_count": 50
        },
        {
            "name": "Product 3",
            "category": "Electronics",
            "price": 599.99,
            "rating": 4.8,
            "ratings_count": 200
        }
    ]
