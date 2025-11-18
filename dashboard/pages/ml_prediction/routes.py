"""
ML Prediction Routes

Handles demand forecasting requests from the dashboard
"""

from flask import render_template, jsonify, request, current_app
from . import ml_prediction_bp
import sys
from pathlib import Path

# Add predictions module to path
predictions_path = Path(__file__).parent.parent.parent.parent / "predictions"
sys.path.insert(0, str(predictions_path))

try:
    from predictor import predictor
    MODELS_AVAILABLE = predictor.models_exist()
except ImportError:
    MODELS_AVAILABLE = False
    predictor = None

@ml_prediction_bp.route('/')
def index():
    """Main prediction page"""

    # Check if models are available
    models_status = {
        'available': MODELS_AVAILABLE,
        'message': 'Model loaded successfully' if MODELS_AVAILABLE else 'Model not trained yet. Please run train_models.py'
    }

    # Get metadata for dropdowns
    metrics = None
    metadata = None
    if MODELS_AVAILABLE:
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
        return jsonify({'error': 'Model not available. Please train model first.'}), 503

    try:
        data = request.get_json()

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
