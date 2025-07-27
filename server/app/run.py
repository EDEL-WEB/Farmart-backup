from flask import Flask
from flask_cors import CORS
from app.config import db, migrate, jwt, Config, api
from app.models import user, cart, animal, order, payment, farmer
from app.controllers.order_controller import OrderController, OrderControllerOne
from app.controllers.payment_controller import PaymentController, PaymentControllerOne
from app.routes import auth_bp, animal_bp, user_bp, cart_bp, farmer_bp, order_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
api.init_app(app)

# CORS setup
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",  # Vite frontend
    "https://your-deployed-frontend.com"  # Deployed frontend
])

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(animal_bp)
app.register_blueprint(user_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(farmer_bp)
app.register_blueprint(order_bp)

# Register API resources
api.add_resource(OrderController, '/orders')
api.add_resource(OrderControllerOne, '/order/<int:id>')
api.add_resource(PaymentController, '/payments')
api.add_resource(PaymentControllerOne, '/payment/<int:id>')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
