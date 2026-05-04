import os
from flask import Flask, render_template, request, jsonify

# Point template and static folders to the frontend directory
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend', static_url_path='')

PRODUCTS = [
    {
        "id": 1,
        "name": "The Cloud Sofa",
        "price": "$2,400",
        "description": "Ultra-soft minimalist sofa designed for unparalleled comfort and sleek aesthetics.",
        "image_url": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 2,
        "name": "Minimalist Oak Table",
        "price": "$1,250",
        "description": "Crafted from sustainable European oak, bringing natural warmth to your dining area.",
        "image_url": "https://images.unsplash.com/photo-1577140917170-285929fb55b7?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 3,
        "name": "Lounge Chair Noir",
        "price": "$890",
        "description": "Premium top-grain leather combined with a matte black steel frame.",
        "image_url": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 4,
        "name": "Scandinavian Bookshelf",
        "price": "$1,100",
        "description": "A refined, open-back shelving unit for displaying your most prized possessions.",
        "image_url": "https://images.unsplash.com/photo-1594620302200-9a762244a156?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 5,
        "name": "Modern Glass Coffee Table",
        "price": "$650",
        "description": "A striking centerpiece featuring tempered glass and brushed brass accents.",
        "image_url": "https://images.unsplash.com/photo-1532372576444-ea23df1f0d36?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 6,
        "name": "Velvet Accent Chair",
        "price": "$780",
        "description": "Luxurious emerald velvet upholstery that adds a pop of sophisticated color.",
        "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 7,
        "name": "Walnut Sideboard",
        "price": "$1,850",
        "description": "Sleek storage solution with push-to-open doors and seamless wood grain.",
        "image_url": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?auto=format&fit=crop&q=80&w=800"
    },
    {
        "id": 8,
        "name": "Bouclé Loveseat",
        "price": "$1,450",
        "description": "Cozy, textured bouclé fabric on a gracefully curved silhouette.",
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&q=80&w=800"
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    
    # Placeholder AI logic
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
