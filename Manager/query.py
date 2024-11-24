import os
from mistralai import Mistral
from tool_config import tools_conf
import json

### IMPORTE NECESSARY FUNCTIONS CALLED IN THE QUERY FUNCTION
# from .... import retrieve_best_productsV0
# from .... import retrieve_best_productsV1
from tools_func import *
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
        self.tools = tools_conf


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
            print("SENDING ")

            response = self.client.chat.complete(
                model = self.agent_id,
                messages = messages,
                tools = self.tools,
                tool_choice = "any",
                )
            
            print("RESPONSE")
            print(response)
            
            if response and response.choices:
                print("RESPONSE is HERE")
                if response.choices[0].message.tool_calls == None:
                    print("No function called")
                    return "No function called", "No parameters"
                function_name = response.choices[0].message.tool_calls[0].function.name
                parameters = response.choices[0].message.tool_calls[0].function.arguments
                
                # Log or handle tool call details
                print(f"Function called: {function_name}")
                print(f"Parameters: {parameters}")
                
                try:
                    parameters_dict = json.loads(parameters)
                except json.JSONDecodeError as e:
                    print(f"Error decoding parameters: {e}")
                    return "error", f"Invalid parameters: {parameters}"

                # Simulate function execution for demo purposes
                if function_name == "retrieve_best_products":
                    # Normally, you'd call the actual function here
                    best_products = fake_retrieve_best_products(parameters)
                    return function_name, best_products
                
                
                elif function_name == "handle_insufficient_info":
                    return function_name, parameters
                
                
                elif function_name == "check_user_purchase_history":
                    user_id = parameters["properties"]["user_id"]
                    k =  parameters["properties"]["k"]
                    history = get_k_purchase(user_id, k)
                    return function_name, history
                
                
                elif function_name == "get_k_nearests_product":
                    print("GET K NEAREST PRODUCT")
                    query = parameters_dict.get("query")
                    k = parameters_dict.get("k", 3)
                    result = get_k_nearests_product(query, k)
                    return function_name, result
                
                elif function_name == "get_k_nearest_users":
                    user_id = parameters["properties"]["user_id"]
                    k = int(parameters["properties"].get("k", 3))
                    nearest_users = get_k_nearest_users(user_id, k)
                    return function_name, nearest_users
                
                elif function_name == "add_purchase":
                    user_id = parameters_dict.get("user_id")
                    product_id = int(parameters_dict.get("product_id", 450))
                    product_name = parameters_dict.get("product_name")
                    result = add_purchase(product_id,product_name, user_id) 
                    return function_name, result
                
                elif function_name == "cancel_purchase":
                    user_id = parameters_dict.get("user_id")
                    purchase_id = int(parameters_dict.get("purchase_id", None))
                    product_name = parameters_dict.get("product_name", None)
                    purchase_date = parameters_dict.get("purchase_date", None)
                    result = cancel_purchase(user_id, purchase_id, product_name, purchase_date) 
                    return function_name, result
                
                elif function_name == "get_best_purchases_from_neighbours":
                    user_id = int(parameters["properties"].get("user_id", 0))
                    best_purchases = get_best_purchases_from_neighbours(user_id)
                    return function_name, best_purchases
                
                
                elif function_name == "get_not_delivered":
                    user_id = int(parameters["properties"]["user_id"])
                    not_delivered = get_not_delivered(user_id)
                    return function_name, not_delivered
                else:
                    return "error", f"Unknown function: {function_name}"
            else:
                print("No response")
                return "error", "I'm sorry, I couldn't generate a response. Please try again."
        except Exception as e:
            print("Error happens when calling the function", e)
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
