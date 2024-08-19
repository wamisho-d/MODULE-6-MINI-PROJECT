# Set Up a Virtual Environment:
# python -m venv venv
# venv\Scripts\activate

# Install Flask and Flask-SQLAlchemy:
# pip install Flask Flask-SQLAlchemy

# Create the Flask Project Structure:
# Set up the basic structure for your Flask project.

  # mkdir e_commerce_app
  # cd e_commerce_app
  # touch app.py
  # mkdir templates static

# Database Design and Schema Creation

#Define the Customer Model:
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/ecommerce_db'
db = SQLAlchemy(app)
class Customer(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    def __repr__(self):
        return f'<Customer{self.name}>'
    
# Define the Product Model:
class product(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.float), nullable=False)
    stock = db.Column(db.Integer, default=0)
    def __repr__(self):
        return f'<Product{self.name}>'

# Define the Order Model:
class product(db.Model):
    id = db.Column(db.integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('order',lazy=True))
    def __repr__(self):
        return f'<Order{self.id}>'

# Create the Database and Tables:
  # Initialize the database and create the tables based on the models.
  # db.create_all()

# Implement CRUD Operations for Customers
# Create a customer (POST/customers/create):
@app.route('/customers/create', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone_number=data['phone_number']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer created sucessfully", "customer_id": new_customer.id}), 201

# Read a Customer(GET/customer/<id>):
@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = customer.query.get(id)
    if not customer:
        return jsonify({"error": customer not found}), 404
    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone_number": customer.phone_number
    })

# Update a Customer (PUT/customers/<id>):
@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = customer.query.get(id)
    if not customer:
        return jsonify({"error": customer not found}), 404
    customer.name = data['name']
    customer.email = data['email']
    customer.phone_number = data['phone_number']
    db.session.commit()
    return jsonify({"message": "Customer updated sucessfully"})

# Delete a Customer (DELETE/customers/<id>):
@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
     customer = customer.query.get(id)
     if not customer:
         return jsonify({"error": "Customer not found"}), 404
     db.session.delete(customer)
     db.session.commit()
     return jsonify({"message": "Customer deleted sucssessfully"})

# Implement CRUD Operations for Products
# Creat a Product (POST/products/create):
@app.route('/products/create', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = product(
        name=data['name'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created sucessfully", "product_id": new_product.id}), 201

# Read a Product (GET/product/<id>):
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    })

# Update a Product(PUT/products/<id>):
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = product.query.get(id)
    if not product:
         return jsonify({"error": "Product not found"}), 404
    product.name = data['name']
    product.price = data['price']
    product.stock = data['stock']

    db.session.commit()
    retrun jsonify({"message": "Product updated sucessfully"})

# Delete a Product(DELETE/product/<id>):
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = product.query.get(id)
    if not product:
         return jsonify({"error": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()
    retrun jsonify({"message": "Product deleted sucessfully"})

# List All Product(GET/products):
@app.route('/products', methods=['GET'])
def list_products():
    products = product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }  for product in products])

@app.route('/orders/create', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(
        customer_id=data['customer_id'],
        order_date=datetime.utcnow()
    )

    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed sucessfully", "order_id": new_order.id}), 201

# Implement Order Processing
# Retrieve an Order(GET/orders/<id>):
@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({
        "id": order.id,
        "customer_id": order.customer_id,
        "order_date": order.order_date
     })

# List All Orders for a Customer(GET/customers/<cusomer_id>/orders):
@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def list_customer_orders(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify([{
        "id": order.id,
        "order_date": order.order_date
    }  for order in customer.orders])










    
    








