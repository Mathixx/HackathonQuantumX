from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import Agent # Enable CORS for all routes

app = Flask(__name__)
CORS(app)

agent = Agent()

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()  # Get the incoming JSON data
    user_message = data.get('message')
    
    # Process the message and get a response (you can integrate your logic here)
    bot_response = agent.get_response_to_user(user_message)

    return jsonify({"response": bot_response})

@app.route('/init-message', methods=['POST'])
def init_message():
    init_message = agent.get_init_message()
    return jsonify({"response": init_message})


@app.route('/get-products', methods=['GET'])
def get_products():
    print("Getting products...")
    products = agent.products
    print("Original Products List:")
    print(products)

    # Transform the products list into a JSON-compatible format
    json_products = [{"name": product[0], "price": product[2]} for product in products]

    print("Transformed JSON Products:")
    print(json_products)

    # Return the JSON object
    return jsonify({"products": json_products})


if __name__ == '__main__':
    app.run(debug=True)