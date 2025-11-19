"""
ML Prediction Routes

Handles demand forecasting requests from the dashboard
Uses external ML API for predictions when deployed
"""

from flask import render_template, jsonify, request, current_app
from . import ml_prediction_bp
import sys
import os
from pathlib import Path
import requests

# Check if we should use external ML API (for Vercel deployment)
ML_API_URL = os.environ.get('ML_API_URL', None)
USE_EXTERNAL_API = ML_API_URL is not None

if not USE_EXTERNAL_API:
    # Local development - load predictor directly
    predictions_path = Path(__file__).parent.parent.parent.parent / "predictions"

    # Check if predictions folder exists (won't exist on Vercel)
    if predictions_path.exists():
        sys.path.insert(0, str(predictions_path))
        try:
            from predictor import predictor
            MODELS_AVAILABLE = predictor.models_exist()
        except ImportError:
            MODELS_AVAILABLE = False
            predictor = None
    else:
        # Predictions folder doesn't exist (probably on Vercel without ML_API_URL set)
        MODELS_AVAILABLE = False
        predictor = None
else:
    # Production - use external API
    try:
        response = requests.get(f"{ML_API_URL}/api/check-models", timeout=5)
        MODELS_AVAILABLE = response.json().get('available', False)
    except:
        MODELS_AVAILABLE = False
    predictor = None

@ml_prediction_bp.route('/')
def index():
    """Main prediction page"""

    # Check if models are available
    models_status = {
        'available': MODELS_AVAILABLE,
        'message': 'Model loaded successfully' if MODELS_AVAILABLE else 'ML Prediction feature is currently unavailable. Please check ML API connection.'
    }

    # Get metadata for dropdowns
    metrics = None
    metadata = None

    if MODELS_AVAILABLE:
        if USE_EXTERNAL_API:
            # Fetch from external API
            try:
                metadata_response = requests.get(f"{ML_API_URL}/api/metadata", timeout=10)
                metrics_response = requests.get(f"{ML_API_URL}/api/metrics", timeout=10)

                if metadata_response.status_code == 200:
                    metadata = metadata_response.json()
                if metrics_response.status_code == 200:
                    metrics = metrics_response.json()
            except Exception as e:
                models_status['available'] = False
                models_status['message'] = f'Failed to connect to ML API: {str(e)}'
        else:
            # Local predictor
            metadata = predictor.get_metadata()
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
        return jsonify({'error': 'Model not available. Please check ML API connection.'}), 503

    try:
        data = request.get_json()

        if USE_EXTERNAL_API:
            # Call external ML API
            response = requests.post(
                f"{ML_API_URL}/api/predict",
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({'error': f'ML API error: {response.text}'}), response.status_code
        else:
            # Local predictor
            result = predictor.predict_demand(
                retailer=data['retailer'],
                region=data['region'],
                product=data['product'],
                sales_method=data['sales_method'],
                price_per_unit=float(data['price_per_unit']),
                month=int(data['month']),
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
