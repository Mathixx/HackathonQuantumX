from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import get_response
from initial_message.initial_message_v0 import get_init_mess
from manager import Manager # Enable CORS for all routes

app = Flask(__name__)
CORS(app)

manager = Manager()

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()  # Get the incoming JSON data
    user_message = data.get('message')
    
    # Process the message and get a response (you can integrate your logic here)
    bot_response = manager.get_response(user_message)

    return jsonify({"response": bot_response})

@app.route('/init-message', methods=['POST'])
def init_message():
    init_message = manager.get_init_message()
    return jsonify({"response": init_message})


@app.route('/get-products', methods=['GET'])
def get_products():
    products = manager.get_products()
    print("prod" )
    print(products)
    return jsonify({"products": products})


if __name__ == '__main__':
    app.run(debug=True)