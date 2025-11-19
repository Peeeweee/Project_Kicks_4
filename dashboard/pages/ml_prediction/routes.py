"""
ML Prediction Routes

Handles demand forecasting requests from the dashboard
Supports both local predictor and external ML API
"""

from flask import render_template, jsonify, request, current_app
from . import ml_prediction_bp
import sys
import os
from pathlib import Path

# Import requests only if needed (avoid errors during Vercel build)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

# Check if we should use external ML API (for Vercel deployment)
ML_API_URL = os.environ.get('ML_API_URL', None)
USE_EXTERNAL_API = ML_API_URL is not None and REQUESTS_AVAILABLE

# Try to load local predictor (for local development)
MODELS_AVAILABLE = False
predictor = None
metadata = None

if not USE_EXTERNAL_API:
    # Local development - load predictor directly
    try:
        predictions_path = Path(__file__).parent.parent.parent.parent / "predictions"
        if predictions_path.exists():
            sys.path.insert(0, str(predictions_path))
            try:
                from predictor import predictor as pred
                predictor = pred
                MODELS_AVAILABLE = predictor.models_exist()
                if MODELS_AVAILABLE:
                    metadata = predictor.get_metadata()
            except ImportError as e:
                print(f"Failed to load local predictor: {e}")
    except Exception as e:
        print(f"Error initializing predictor: {e}")
else:
    # Production - use external API
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(f"{ML_API_URL}/api/check-models", timeout=5)
            MODELS_AVAILABLE = response.json().get('available', False)

            # Get metadata from API
            if MODELS_AVAILABLE:
                metadata_response = requests.get(f"{ML_API_URL}/api/metadata", timeout=5)
                metadata = metadata_response.json()
    except Exception as e:
        print(f"Failed to connect to ML API: {e}")
        MODELS_AVAILABLE = False

@ml_prediction_bp.route('/')
def index():
    """Main prediction page"""

    # Check if models are available
    models_status = {
        'available': MODELS_AVAILABLE,
        'message': 'Model loaded successfully' if MODELS_AVAILABLE else 'ML Prediction feature is currently unavailable.'
    }

    # Get metrics
    metrics = None
    if MODELS_AVAILABLE:
        if USE_EXTERNAL_API:
            try:
                response = requests.get(f"{ML_API_URL}/api/metrics", timeout=5)
                metrics = response.json()
            except:
                pass
        else:
            if predictor:
                metrics = predictor.get_metrics()

    return render_template(
        'ml_prediction/index.html',
        models_status=models_status,
        metadata=metadata,
        metrics=metrics
    )

@ml_prediction_bp.route('/api/predict-demand', methods=['POST'])
def predict_demand():
    """API endpoint to predict Units Sold and calculate Total Sales"""

    if not MODELS_AVAILABLE:
        return jsonify({'error': 'Model not available.'}), 503

    try:
        data = request.get_json()

        if USE_EXTERNAL_API:
            # Forward request to external ML API
            response = requests.post(
                f"{ML_API_URL}/api/predict-demand",
                json=data,
                timeout=30
            )
            return jsonify(response.json()), response.status_code
        else:
            # Use local predictor
            result = predictor.predict_demand(
                retailer=data['retailer'],
                region=data['region'],
                product=data['product'],
                sales_method=data['sales_method'],
                price_per_unit=float(data['price_per_unit']),
                month=data['month'],  # Can be month name or number
                quarter=int(data['quarter'])
            )
            return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ml_prediction_bp.route('/api/check-models')
def check_models():
    """Check if models are available"""
    return jsonify({
        'available': MODELS_AVAILABLE,
        'message': 'Model ready' if MODELS_AVAILABLE else 'Model not trained'
    })
