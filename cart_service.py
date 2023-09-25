import requests
from flask import Flask, jsonify, request


app = Flask(__name__)


customers = [
    {
     "user": "ams165",
     "cart": [
        {"id": 1, "name": "banana", "price": 0.46, "quantity": 2},
        {"id": 2, "name": "apple", "price": 0.75, "quantity": 3}
     ]
    }
]

@app.route('/cart/<string:user_id>', methods=['GET'])
def get_cart(user_id):
    customer = next((customer for customer in customers if customer["user"] == user_id), None)
    if customer:
        return jsonify({"customer": customer})
    else:
        return jsonify({"error": "Task not found"}), 404
    
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def addToCart(product_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    data = response.json()

    customers[0]['cart'][product_id-1]['price'] += data["product"]["price"]
    customers[0]['cart'][product_id-1]['quantity'] += 1

    requests.post(f'http://127.0.0.1:5000/remove/{product_id}')
    return jsonify({"message": "Product added"})

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def removeFromCart(product_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    data = response.json()
   
    customers[0]['cart'][product_id-1]['price'] -= data["product"]["price"]
    customers[0]['cart'][product_id-1]['quantity'] -= 1

    requests.post(f'http://127.0.0.1:5000/add/{product_id}')
    return jsonify({"message": "Product removed"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)