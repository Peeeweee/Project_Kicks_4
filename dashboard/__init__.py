# /dashboard/__init__.py

from flask import Flask
import os
from .data_loader import load_data

def create_app():
    """Create and configure an instance of the Flask application."""
    # Create the Flask app instance, specifying the top-level template folder
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'adidas-kicks-dashboard-2024'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Load the data and attach it to the app context
    data_path = os.path.join(app.root_path, '..', 'data', 'adidas_sales_cleaned.csv')
    app.df = load_data(data_path)
    
    # Define color constants and attach to app context
    app.COLORS = {
        'primary': '#000000', 'secondary': '#FFFFFF', 'accent': '#767676',
        'success': '#00A651', 'info': '#0057B8', 'warning': '#FDB913', 'danger': '#E4002B'
    }
    app.CHART_COLORS = ['#000000', '#0057B8', '#00A651', '#FDB913', '#E4002B', '#767676', '#4A90E2', '#50C878']

    with app.app_context():
        # --- Register Blueprints ---

        # Register the API blueprint
        from .api import bp as api_bp
        app.register_blueprint(api_bp)

        # Register all the page blueprints
        from .pages.sales import bp as sales_bp
        from .pages.product import bp as product_bp
        from .pages.customer import bp as customer_bp
        from .pages.ml_prediction import ml_prediction_bp
        from .pages.about import bp as about_bp

        app.register_blueprint(sales_bp)
        app.register_blueprint(product_bp)
        app.register_blueprint(customer_bp)
        app.register_blueprint(ml_prediction_bp)
        app.register_blueprint(about_bp)

    return app