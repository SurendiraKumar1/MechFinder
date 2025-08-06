MechFinder 🔧
One-line description: A location-based web platform that connects vehicle owners with nearby mechanic shops through interactive maps and shop management dashboards.
About the Project
MechFinder is a full-stack web application that solves the common problem of finding reliable mechanic shops in your area. Built with Flask and MongoDB, it provides an intuitive platform where users can discover nearby automotive service providers while allowing shop owners to manage their business listings.
Why MechFinder?

Real Problem, Real Solution: Finding trustworthy mechanics nearby is often challenging, especially in unfamiliar areas
Two-Way Platform: Serves both customers looking for services and shop owners wanting to expand their reach
Location-Centric: Uses interactive maps to provide accurate, location-based results
Simple & Accessible: Clean interface that works across devices

Key Features
For Customers

🗺️ Interactive Map Interface - Visualize all registered mechanic shops on an interactive map
📍 Location-Based Search - Find shops near your current location
📋 Shop Details - View services, working hours, contact information, and addresses
📱 Responsive Design - Works seamlessly on desktop and mobile devices

For Shop Owners

🏪 Shop Registration - Easy signup process with location selection on map
🔐 Secure Dashboard - Password-protected area to manage shop information
✏️ Real-time Updates - Modify shop details, services, and working hours anytime
📊 Business Management - Track and update business information efficiently

Technology Stack

Backend: Flask (Python)
Database: MongoDB with PyMongo
Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
Maps: Leaflet.js with OpenStreetMap
Authentication: Flask-Login with password hashing
Styling: Custom CSS with Bootstrap components

How It Works

Shop Registration: Mechanic shop owners register by providing business details and selecting their location on an interactive map
Map Visualization: All registered shops appear as markers on the main map interface
Shop Discovery: Users can browse the map, click on markers to view shop details
Information Access: Each shop marker displays services, working hours, contact details, and address
Shop Management: Registered shop owners can log in to update their information anytime

Installation & Setup

Clone the repository
bashgit clone <repository-url>
cd mechfinder

Install dependencies
bashpip install flask flask-pymongo flask-login flask-cors python-dotenv werkzeug

Set up environment variables
Create a .env file:
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://localhost:27017/mechanic_finder

Start MongoDB service
bashmongod

Run the application
bashpython app.py

Access the application
Open http://localhost:5000 in your browser

Project Structure
mechfinder/
├── app.py                 # Main Flask application
├── static/
│   ├── css/style.css     # Custom styling
│   └── js/map.js         # Map functionality
├── templates/
│   ├── base.html         # Base template
│   ├── home.html         # Landing page
│   ├── register.html     # Shop registration
│   ├── login.html        # Shop login
│   ├── dashboard.html    # Shop management
│   └── map.html          # Map interface
└── README.md
API Endpoints

GET /api/shops - Retrieve all registered shops
GET /api/shop/<shop_id> - Get specific shop details
POST /register - Register new mechanic shop
POST /login - Shop owner authentication
POST /update_shop - Update shop information

Future Enhancements

User reviews and ratings system
Advanced search filters (service type, price range)
Appointment booking functionality
Mobile app development
Integration with navigation apps

Contributing
Feel free to fork this project and submit pull requests for any improvements!
License
This project is open source and available under the MIT License.
