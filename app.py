from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mechanic_finder')
CORS(app)

# Initialize MongoDB
mongo = PyMongo(app)

# Initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.id = str(user_data['_id'])
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    shop = mongo.db.shops.find_one({'_id': ObjectId(user_id)})
    return User(shop) if shop else None

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        shop_data = request.form.to_dict()
        
        # Check if email exists
        if mongo.db.shops.find_one({'email': shop_data['email']}):
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        # Insert into MongoDB
        new_shop = {
            'shop_name': shop_data['shop_name'],
            'owner_name': shop_data['owner_name'],
            'email': shop_data['email'],
            'password_hash': generate_password_hash(shop_data['password']),
            'phone': shop_data['phone'],
            'address': shop_data['address'],
            'latitude': float(shop_data['latitude']),
            'longitude': float(shop_data['longitude']),
            'services': shop_data['services'],
            'working_hours': shop_data['working_hours']
        }
        
        mongo.db.shops.insert_one(new_shop)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        shop = mongo.db.shops.find_one({'email': email})
        
        if shop and check_password_hash(shop['password_hash'], password):
            user = User(shop)
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    shop = mongo.db.shops.find_one({'_id': ObjectId(current_user.id)})
    return render_template('dashboard.html', shop=shop)

# Update Shop Details
@app.route('/update_shop', methods=['POST'])
@login_required
def update_shop():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        update_data = {
            'shop_name': form_data['shop_name'],
            'phone': form_data['phone'],
            'address': form_data['address'],
            'services': form_data['services'],
            'working_hours': form_data['working_hours']
        }
        
        if form_data.get('latitude') and form_data.get('longitude'):
            update_data['latitude'] = float(form_data['latitude'])
            update_data['longitude'] = float(form_data['longitude'])
        
        mongo.db.shops.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$set': update_data}
        )
        
        flash('Shop details updated successfully!', 'success')
        return redirect(url_for('dashboard'))

# Map Page Route
@app.route('/map')
def map_view():
    return render_template('map.html')

# Fetch all registered shops
@app.route('/api/shops', methods=['GET'])
def get_shops():
    shops = list(mongo.db.shops.find({}, {
        'password_hash': 0
    }))

    # Convert ObjectId to string for JSON serialization
    for shop in shops:
        shop['_id'] = str(shop['_id'])
    
    return jsonify(shops)

# Fetch single shop
@app.route('/api/shop/<shop_id>', methods=['GET'])
def get_shop(shop_id):
    shop = mongo.db.shops.find_one({'_id': ObjectId(shop_id)}, {
        'password_hash': 0
    })
    if shop:
        shop['_id'] = str(shop['_id'])
        return jsonify(shop)
    return jsonify({'error': 'Shop not found'}), 404

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
