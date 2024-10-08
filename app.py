from flask import Flask, request, jsonify
from db_setup import db  # Import db from db_setup.py
from seller import Seller
from product import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dbuserdbuser@34.173.164.27/Seller_Service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize db with the Flask app


# Index route
@app.route('/')
def index():
    return 'Welcome to the Seller Service API!'

# Test database connection route
@app.route('/test-db-connection', methods=['GET'])
def test_db_connection():
    try:
        sellers = Seller.query.all()
        return jsonify({"message": "Database connection successful", "sellers": len(sellers)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register a new seller
@app.route('/seller/register', methods=['POST'])
def register_seller():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    new_seller = Seller(name=name, email=email)
    db.session.add(new_seller)
    db.session.commit()

    return jsonify(new_seller.register_seller()), 201

# Create a new product
@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    seller_id = data.get('seller_id')
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    description = data.get('description')
    category = data.get('category')

    seller = Seller.query.get(seller_id)
    if not seller:
        return jsonify({"error": "Seller not found"}), 404

    new_product = Product(seller_id=seller.id, name=name, price=price, stock=stock, description=description, category=category)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created successfully.", "product_id": new_product.id}), 201

# Main entry point for creating tables and running the app
if __name__ == '__main__':
    # This will create all tables based on the models defined in your app
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=8000, debug=True)
