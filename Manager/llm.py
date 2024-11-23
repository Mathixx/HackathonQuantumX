from mistralai import Mistral

api_key = "W7jZ5RO87zVxhO0gehFjjg0TqyXasmGj"
model = "mistral-small-latest"

def get_response(user_message):
    client = Mistral(api_key=api_key)
    messages = [{"role": "user", "content": user_message}]
    response = client.chat.complete(
        model = model,
        messages = messages
    )
    return response.choices[0].message.content

