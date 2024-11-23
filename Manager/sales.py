import os
from mistralai import Mistral

# Retrieve the API key from the environment variable
api_key = "W7jZ5RO87zVxhO0gehFjjg0TqyXasmGj"
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Define the custom agent ID TO CHANGE
custom_agent_id ="mistral-small-latest" #"ag:68495cb5:20241123:expert-tpmc:bbd4e63b"

class Sales:
    def __init__(self):
        """
        Initialize the Sales class with a specific agent ID and client.

        :param agent_id: The custom agent ID for Mistral AI.
        :param client: The Mistral client instance.
        """
        self.agent_id = custom_agent_id
        self.client = Mistral(api_key=api_key)


    def get_response(self, user_query):
        """
        Get skincare advice based on the user's query.

        :param user_query: A string containing the user's question or concern about skincare.
        :return: A string with the AI's response or an error message if the response fails.
        """
        messages = [
            {
                "role": "user",
                "content": user_query
            }
        ]

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

