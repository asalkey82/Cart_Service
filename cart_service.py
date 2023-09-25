import requests
from flask import Flask, jsonify, request


app = Flask(__name__)


customers = [
    {
     "user": 1,
     "cart": [
        {"id": 1, "name": "banana", "price": 0.46, "quantity": 2},
        {"id": 2, "name": "apple", "price": 0.75, "quantity": 3}
     ]
    }
]

BASE_URL = "https://carl-mart.onrender.com"

#Endpoint 1: get user cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    customer = next((customer for customer in customers if customer["user"] == user_id), None)
    if customer:
        return jsonify({"customer": customer})
    else:
        return jsonify({"error": "Customer not found"}), 404

#Endpoint 2: Add product to user cart. 
#Makes another call to product server to remove product from store
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def addToCart(product_id, user_id):
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    data = response.json()

    customers[user_id-1]['cart'][product_id-1]['price'] += data["product"]["price"]
    customers[user_id-1]['cart'][product_id-1]['quantity'] += 1

    requests.post(f'{BASE_URL}/remove/{product_id}')
    return jsonify({"message": "Product added"})

#Endpoint 3: Remove product from user cart. 
#Makes another call to product server to add product to store
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def removeFromCart(product_id, user_id):
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    data = response.json()
   
    customers[user_id-1]['cart'][product_id-1]['price'] -= data["product"]["price"]
    customers[user_id-1]['cart'][product_id-1]['quantity'] -= 1

    requests.post(f'{BASE_URL}/add/{product_id}')
    return jsonify({"message": "Product removed"})

if __name__ == '__main__':
    app.run(debug=True)
