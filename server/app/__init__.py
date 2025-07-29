import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, jwt

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
        static_url_path='/static'
    )

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS configuration
    CORS(app,
     supports_credentials=True,
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type", "Authorization", "Set-Cookie"]
)


    # Add response headers after each request
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Vary'] = 'Origin'
        return response

    # Import models
    from app.models.user import User
    from app.models.animal import Animal
    from app.models.cart import Cart
    from app.models.order import Order
    from app.models.payment import Payment

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.animal_routes import animal_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.farmer_routes import farmer_bp
    from app.routes.order_routes import order_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.user_routes import user_bp
    from app.routes.upload_routes import upload_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(animal_bp, url_prefix='/api/animals')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(farmer_bp, url_prefix="/api/farmers")
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(upload_bp)

    # Static image file route
    @app.route('/images/<path:filename>')
    def serve_images(filename):
        images_dir = os.path.join(app.static_folder, 'images')
        return send_from_directory(images_dir, filename)

    # Fallback for broken image paths
    @app.route('/fallback.jpg')
    def serve_fallback():
        return send_from_directory(app.static_folder, 'fallback.jpg')

    # Handle image 404s with fallback
    @app.errorhandler(404)
    def handle_404(e):
        if '/images/' in str(e) or '.jpg' in str(e) or '.png' in str(e):
            try:
                return send_from_directory(app.static_folder, 'fallback.jpg')
            except:
                pass
        return e

    return app

# Entry point
app = create_app()


