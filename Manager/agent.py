from mistralai import Mistral
import tool_config 
import json
from recommendation_user import get_best_purchases_from_neighbours
### IMPORTE NECESSARY FUNCTIONS CALLED IN THE QUERY FUNCTION
# from .... import retrieve_best_productsV0
# from .... import retrieve_best_productsV1
import tools_func
# Retrieve the API key from the environment variable
api_key = "W7jZ5RO87zVxhO0gehFjjg0TqyXasmGj"
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")
custom_agent_id = "ag:68495cb5:20241123:expert-tpmc:bbd4e63b"



class Agent:
    def __init__(self):
        self.products = []
        self.cart = []
        self.memory = ""
        self.client = Mistral(api_key=api_key)
        self.tools = tool_config.tools_conf
        self.names_to_functions = tools_func.names_to_functions
        self.agent_id = custom_agent_id
        self.user_id = 0
        self.user_query = ""
        self.data = ""
        self.advice = ""
        self.next_data_query = ""
        self.expert_input = ""
        self.querry_data = ""
        
    def reset(self):
        self.products = []
        self.cart = []
        self.memory = ""
        self.user_query = ""
        self.data = ""
        self.advice = ""
        self.next_data_query = ""
        self.expert_input = ""
        self.querry_data = ""

    def get_response_to_user(self, user_message):
        self.user_query = user_message
        self.memory = self.memory + " user :  " + user_message
        self.build_expert_input()
        thinking_lim = 1
        self.querry_data = ""
        while self.querry_data != "STOP" and thinking_lim > 0:
            self.update_advice()
            print("1 : " , self.expert_input)
            self.get_next_querry()
            print("2 : " , self.expert_input)
            self.get_next_action()
            print("3 : " , self.expert_input)
            self.update_data(self.querry_data)
            print("4 : " , self.expert_input)
            thinking_lim -= 1
        resp = self.get_response()
        self.memory = self.memory + " agent :  " + resp
        return resp

        
    def build_expert_input(self):
        print("Building expert input")
        """print("user input :", self.expert_input)
        if self.expert_input != "":
            # Parse the existing expert input as JSON
            # Clean up the extra enclosing quotes and line breaks
            cleaned_json_string = self.expert_input.strip('```json\n').strip('\n```') 
            json_expert_input = json.loads(cleaned_json_string)
            self.data = json_expert_input.get("data_available", "")
        else:
            # Initialize self.data if not already set
            self.data = """

        #  Construct the new expert input as a JSON string
        self.expert_input = json.dumps({
            "user_input": self.user_query,
            "data_available": self.data,
            "Advice": self.advice,
            "new_data_query": self.next_data_query
        })   

    def update_advice(self):
        task = "based on the current input, updcate the advice to be made for the customer. Answer should be in the right format. Only the advice should be updated, and not the other fields. Answer should kept short. Don't make it too long. Go straight to the point."
        txt_message = "Here are the previous messages : " + self.memory + " ." + task + "  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        self.expert_input = agent_response.choices[0].message.content

    def update_data(self, data):
        task = "Update the data_available field with labeled data from external_data. Use descriptive tags based on the external_data type (e.g., '#product suggestions' or 'previously bought products'). Retain existing data_available content. Clear the new_data_query field after updating. Modify only data_available and new_data_query. Ensure the response reflects these changes" #The goal is to update the data_available field with new data received through external data. The data_available field should now include this new data, appropriately labeled. For example, if the query suggests products, add the list of products to data_available, labeling it as 'product suggestion'. Instructions: Update data_available with the information from the external data field. Each addition should be labeled with a descriptive tag, based on the external data tag. Be very precise. For example, Suggested products and previously bought products shouldbe labeled differently .Clear the new_data_query field after updating data_available. This field should be set to empty as a result of this operation.Do not modify any other fields besides data_available and new_data_query.Your response should reflect these changes, with data_available updated and new_data_query cleared. Do not remove any information which was the data_available field. "
        txt_message = task + " External data : " + data + "  Current fields :  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        self.expert_input = agent_response.choices[0].message.content
        
    def get_next_action(self):
        task = "Extract the `new_data_query` field from the input, determine the appropriate function to call based on its content, and extract its parameters. Discard other fields. Format the action as a function call with the chosen function and parameters." #"From this input state, extract the content of the 'new_data_query' field, and use it to decide what action to take next. The action should be a function call, with the right parameters. The function to call should be chosen based on the new_data_query field. The parameters should be extracted from the new_data_query field. The other fields should be discarded. The action should be in the right format. "


        txt_message = task + " Here is the input state :   " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]
    
        
        response = self.client.chat.complete(
                model = "mistral-large-latest",
                messages = messages,
                tools = self.tools,
                tool_choice = "any",
                )
        function_name = response.choices[0].message.tool_calls[0].function.name
        print("function_name : ", function_name)
        function_params = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        if function_name == "get_k_nearests_product":
            print("I AM LOOKING FOR PRODUCTS")
            new_products, self.querry_data = self.names_to_functions[function_name](**function_params)
            if new_products != []:
                self.products = new_products
        elif function_name == "add_to_cart":
            print("I AM ADDING TO CART")
            new_cart, self.querry_data = self.names_to_functions[function_name](**function_params)
            for c in new_cart:
                self.cart.append(c)
        else:
            _ , self.querry_data = self.names_to_functions[function_name](**function_params)

    
    def get_next_querry(self):
        task =  "Generate the next `data_query` based on client input and available data. Use action verbs (e.g., 'Find', 'Identify') to specify what needs to be queried. Leave `data_query` empty if the required information is already available. Request only missing information, prioritizing suitable products for the user if none are identified. Focus each query on a single piece of information. Avoid requesting products already in `available_data`. Ensure the query enables the query agent to select the correct function and arguments. Modify only the `data_query` field, stopping when all necessary data is gathered."#"Based on the client input and the available data, generate the next data query to be made. The query should use action verbs (e.g., 'Find', 'Identify') to clearly indicate what needs to be queried. If the required information is already available, leave the data query field empty.Only request the information that is still needed, and avoid asking for unnecessary details. When possible, prioritize looking for products that may be suitable for the user, especially if none have been identified yet. Ensure that each query is focused on one specific piece of information at a time.If products are already in availble_data, you should not request them again. The query should contain all necessary information for the query agent to select the correct function and provide the right argument. The response should be in the correct format, modifying only the data_query field, and should stop once all necessary data has been gathered."
        txt_message = task + "  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        self.expert_input = agent_response.choices[0].message.content

    def get_response(self):
        task = "It seems all the information that could be obtained from the data base is in your possessing. Based on the current input, get the response to be made to the customer. Answer should be a string understandable by the client. Data querry should now be empty, as the information is transfered from there to available data Write it as it will be read by the client, do not show internal dialog. "
        txt_message = "Here are the previous messages : " + self.memory + " ." + task + "  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        return agent_response.choices[0].message.content
    
    def get_init_message(self): 
        # recommendation, text = get_best_purchases_from_neighbours(self.user_id)
        # self.products = recommendation
        
        return f"Hello! I am your personnal assistant for today. How can I help you ?"
