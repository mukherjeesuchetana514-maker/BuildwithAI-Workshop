import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Point template and static folders to the frontend directory
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend', static_url_path='')
app.secret_key = 'mukherjee_paljichar_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    is_wishlist = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

with app.app_context():
    db.create_all()
    if not User.query.first():
        dummy_user = User(email='user@example.com', password='password123')
        db.session.add(dummy_user)
        db.session.commit()
    
    if not Product.query.first():
        products_data = [
            {"name": "The Cloud Sofa", "category": "Sofas", "price": "$2,400", "description": "Ultra-soft minimalist sofa designed for unparalleled comfort and sleek aesthetics.", "image_url": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&q=80&w=800"},
            {"name": "Velvet Loveseat", "category": "Sofas", "price": "$1,450", "description": "Cozy, textured velvet fabric on a gracefully curved silhouette.", "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&q=80&w=800"},
            {"name": "Modern Leather Sectional", "category": "Sofas", "price": "$3,200", "description": "Premium top-grain leather sectional, perfect for spacious living rooms.", "image_url": "/leather_sectional.png"},
            
            {"name": "Minimalist Oak Table", "category": "Tables", "price": "$1,250", "description": "Crafted from sustainable European oak, bringing natural warmth to your dining area.", "image_url": "https://images.unsplash.com/photo-1577140917170-285929fb55b7?auto=format&fit=crop&q=80&w=800"},
            {"name": "Modern Glass Coffee Table", "category": "Tables", "price": "$650", "description": "A striking centerpiece featuring tempered glass and brushed brass accents.", "image_url": "/glass_coffee_table.png"},
            {"name": "Walnut Dining Table", "category": "Tables", "price": "$1,800", "description": "Large dining table for 8, crafted from rich walnut wood.", "image_url": "https://images.unsplash.com/photo-1604578762246-41134e37f9cc?auto=format&fit=crop&q=80&w=800"},
            
            {"name": "Lounge Chair Noir", "category": "Chairs", "price": "$890", "description": "Premium top-grain leather combined with a matte black steel frame.", "image_url": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80&w=800"},
            {"name": "Velvet Accent Chair", "category": "Chairs", "price": "$780", "description": "Luxurious emerald velvet upholstery that adds a pop of sophisticated color.", "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&q=80&w=800"},
            {"name": "Ergonomic Office Chair", "category": "Chairs", "price": "$550", "description": "Sleek and comfortable, designed for long hours of productive work.", "image_url": "https://images.unsplash.com/photo-1505797149-43b0069ec26b?auto=format&fit=crop&q=80&w=800"},

            {"name": "Scandinavian Bookshelf", "category": "Cupboards", "price": "$1,100", "description": "A refined, open-back shelving unit for displaying your most prized possessions.", "image_url": "https://images.unsplash.com/photo-1594620302200-9a762244a156?auto=format&fit=crop&q=80&w=800"},
            {"name": "Walnut Sideboard", "category": "Cupboards", "price": "$1,850", "description": "Sleek storage solution with push-to-open doors and seamless wood grain.", "image_url": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?auto=format&fit=crop&q=80&w=800"},
            {"name": "Minimalist Wardrobe", "category": "Cupboards", "price": "$2,100", "description": "Spacious and modern wardrobe to elegantly store your clothing.", "image_url": "https://images.unsplash.com/photo-1558997519-83ea9252edf8?auto=format&fit=crop&q=80&w=800"}
        ]
        for p in products_data:
            db.session.add(Product(**p))
        db.session.commit()

@app.route('/')
def index():
    category = request.args.get('category')
    if category and category != 'All':
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('index.html', products=products, selected_category=category or 'All')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = 1
    item = CartItem(user_id=user_id, product_id=product_id, is_wishlist=False)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/add-to-wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    user_id = 1
    item = CartItem(user_id=user_id, product_id=product_id, is_wishlist=True)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    user_id = 1
    cart_items = CartItem.query.filter_by(user_id=user_id, is_wishlist=False).all()
    wishlist_items = CartItem.query.filter_by(user_id=user_id, is_wishlist=True).all()
    
    total_price = 0
    for item in cart_items:
        price_str = item.product.price.replace('$', '').replace(',', '')
        try:
            total_price += float(price_str)
        except ValueError:
            pass
    total_price_formatted = f"${total_price:,.2f}"
    
    return render_template('cart.html', cart_items=cart_items, wishlist_items=wishlist_items, total_price=total_price_formatted)

@app.route('/move-to-cart/<int:item_id>', methods=['POST'])
def move_to_cart(item_id):
    item = db.session.get(CartItem, item_id)
    if item and item.user_id == 1:
        item.is_wishlist = False
        db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/move-to-wishlist/<int:item_id>', methods=['POST'])
def move_to_wishlist(item_id):
    item = db.session.get(CartItem, item_id)
    if item and item.user_id == 1:
        item.is_wishlist = True
        db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/remove-item/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    item = db.session.get(CartItem, item_id)
    if item and item.user_id == 1:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
        
    user_id = 1
    CartItem.query.filter_by(user_id=user_id, is_wishlist=False).delete()
    db.session.commit()
    return redirect(url_for('order_success'))

@app.route('/order-success')
def order_success():
    return render_template('order_success.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    
    if 'sofa' in user_message or 'loveseat' in user_message:
        reply = "Our minimalist sofas and loveseats are designed for maximum comfort. Are you looking for a specific color?"
    elif 'table' in user_message or 'desk' in user_message:
        reply = "We have stunning oak and glass tables that fit perfectly in modern spaces."
    elif 'price' in user_message or 'cost' in user_message:
        reply = "Prices vary by piece, but everything in our collection is crafted with premium materials to ensure lasting value."
    else:
        reply = "Welcome to MUKHERJEE FURNITURE! I'm your digital assistant. How can I help you furnish your space today?"
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
