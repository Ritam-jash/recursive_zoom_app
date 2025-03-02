from flask import Flask

def create_app():
    """Initialize the Flask app"""
    app = Flask(__name__)

    with app.app_context():
        # Import routes
        from app import routes
        
        return app
