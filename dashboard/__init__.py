# /dashboard/__init__.py

from flask import Flask
import os
import sys
import traceback

def create_app():
    """Create and configure an instance of the Flask application."""
    try:
        # Create the Flask app instance, specifying the top-level template folder
        app = Flask(__name__, instance_relative_config=True)
        app.config['SECRET_KEY'] = 'adidas-kicks-dashboard-2024'
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

        # Ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # Load the data and attach it to the app context
        # Use absolute path from project root for better compatibility with Vercel
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(project_root, 'data', 'adidas_sales_cleaned.csv')

        print(f"Looking for data file at: {data_path}")
        print(f"Project root: {project_root}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"__file__: {__file__}")

        # Verify the file exists
        if not os.path.exists(data_path):
            print(f"ERROR: Data file not found at: {data_path}")
            print(f"Files in project root: {os.listdir(project_root)}")
            if os.path.exists(os.path.join(project_root, 'data')):
                print(f"Files in data directory: {os.listdir(os.path.join(project_root, 'data'))}")
            raise FileNotFoundError(f"Data file not found at: {data_path}")

        from .data_loader import load_data
        app.df = load_data(data_path)
        print(f"Successfully loaded data with {len(app.df)} rows")

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

        print("Flask app created successfully!")
        return app

    except Exception as e:
        print(f"ERROR in create_app: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        raise