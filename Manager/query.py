import os
from mistralai import Mistral
from tool_config import tools_conf

### IMPORTE NECESSARY FUNCTIONS CALLED IN THE QUERY FUNCTION
# from .... import retrieve_best_productsV0
# from .... import retrieve_best_productsV1
from tools_func import get_k_purchase
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
