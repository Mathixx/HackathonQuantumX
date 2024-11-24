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
custom_agent_id = "ag:68495cb5:20241123:expert-tpmc:bbd4e63b"




class Agent:
    def __init__(self,tools_conf,names_to_functions):
        self.products = []
        self.client = Mistral(api_key=api_key)
        self.tools = tools_conf
        self.names_to_functions = names_to_functions
        self.agent_id = custom_agent_id

        self.user_query = ""
        self.data = ""
        self.advice = ""
        self.next_data_query = ""
        self.expert_input = ""
        self.querry_data = ""

    def get_response_to_user(self, user_message):
        self.user_query = user_message
        self.build_expert_input()
        while self.querry_data != "STOP":
            self.update_advice()
            self.get_next_querry()
            self.get_next_action()
            self.update_data(self.querry_data)
        return self.get_reseponse()

        
    def build_expert_input(self):
        self.expert_input = "{\"user_input\": \"" + self.user_query + "\"; \"data_available\": \"" + self.data + "\"; \"Advice\": \"" + self.advice + "\"; \"new_data_query\": \"" + self.next_data_query + "\"}"
        

    def update_advice(self):
        task = "based on the current input, update the advice to be made for the customer. Answer should be in the right format. Only the advice should be updated, and not the other fields"
        txt_message = task + "  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        self.expert_input = agent_response.choices[0].message.content

    def update_data(self, data):
        task = "The goal is to update the data_available field with new data received through external data. The data_available field should now include this new data, appropriately labeled. For example, if the query suggests products, add the list of products to data_available, labeling it as 'product suggestion'. Instructions: Update data_available with the information from the external data field. Each addition should be labeled with a descriptive tag, based on the external data tag. Be very precise. For example, Suggested products and previously bought products shouldbe labeled differently .Clear the new_data_query field after updating data_available. This field should be set to empty as a result of this operation.Do not modify any other fields besides data_available and new_data_query.Your response should reflect these changes, with data_available updated and new_data_query cleared. Do not remove any information which was the data_available field. "
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
        task = "From this inpu state, extract the content of the 'new_data_query' field, and use it to decide what action to take next. The action should be a function call, with the right parameters. The function to call should be chosen based on the new_data_query field. The parameters should be extracted from the new_data_query field. The other fields should be discarded. The action should be in the right format. "


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
        function_params = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(function_name)
        print(function_params)
        self.querry_data = self.names_to_functions[function_name](**function_params)
        
    
    def get_next_querry(self):
        task = "based on the client input, and the available data, get the next data query to be made. Use actions, verbs, to indicate what should be querried, such as Find... Indentify... . If we already have the needed information, the data querry can be empty, 'no more information needed'. Take into account all the available data and advcie. Dont ask more than needed. You should stop at some point. Only look for information that you don't already have. When possible, try to look for products that might be good for the user, if none have been identified yet. The query should contain all the necessary information for the querry agent to choose the right function to call and give the right argument. Be precise. Only lookf for one information at a time. Only modify the querry data field.  Answer should be in the right format. "
        txt_message = task + "  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        self.expert_input = agent_response.choices[0].message.content

    def get_reseponse(self):
        task = "It seems all the information that could be obtained from the data base is in your possessing. Based on the current input, get the response to be made to the customer. Answer should be a string understandable by the client. Data querry should now be empty, as the information is transfered from there to available data. "
        txt_message = task + "  " + self.expert_input
        messages = [
            {
                "role": "user",
                "content": txt_message
            }
        ]

        agent_response = self.client.agents.complete(agent_id=self.agent_id, messages=messages)
        self.expert_input = agent_response.choices[0].message.content
        return self.expert_input