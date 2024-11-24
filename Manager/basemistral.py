
import os
from mistralai import Mistral

# Retrieve the API key from the environment variable
api_key = "W7jZ5RO87zVxhO0gehFjjg0TqyXasmGj"
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Define the custom agent ID
# custom_agent_id = "ag:68495cb5:20241123:expert-tpmc:bbd4e63b"
custom_agent_id = "mistral-small-latest"

class BaseMistral:
    def __init__(self):
        """
        Initialize the base mistral user for simple case 

        :param agent_id: The custom agent ID for Mistral AI.
        :param client: The Mistral client instance.
        """
        self.agent_id = custom_agent_id
        self.client = Mistral(api_key=api_key)
        
    def get_user_info(self, conversation: list[dict], user_info: str )-> str :
        """Generate a small paragraph of informations based on a conversation of an user and the LLM and the already known informations 

        Args:
            conversations (dict[str])
            user_info 
        Returns:
            str: _description_
        """
    
        query = f"Context: Below is a paragraph describing a user's habits and preferences, followed 
        by a conversation between the user and a retail sales agent. 
        Analyze the conversation to identify any new information about the user's habits or preferences 
        and incorporate these updates into the existing paragraph. Ensure the updated paragraph reflects the most accurate 
        and detailed habits of the user. \n Guidelines: \nFocus on extracting key details about the user's habits from the conversation.
                Prioritize new and relevant information, ensuring it aligns with the context of the paragraph.
                Rewrite the paragraph seamlessly to include these updates, keeping the tone consistent. \n Task: \n Original paragraph : {user_info}"

        messages = conversation.append({"role" : "user", "content": query})  
        
        
        try:
            # Send the query to the custom agent
            response = self.client.chat.complete(model=self.agent_id, messages=messages)

            # Extract the assistant's reply
            if response and response.choices:
                return response.choices[0].message.content
            else:
                return "I'm sorry, I couldn't generate a response. Please try again."
        except Exception as e:
            return f"An error occurred: {e}"