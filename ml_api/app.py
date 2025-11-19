"""
ML Prediction API - Standalone Flask API for model predictions
Deploy this separately on Render, Railway, or Heroku
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add predictions module to path
predictions_path = Path(__file__).parent.parent / "predictions"
sys.path.insert(0, str(predictions_path))

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from Vercel

# Import predictor
try:
    from predictor import predictor
    MODELS_AVAILABLE = predictor.models_exist()
except ImportError:
    MODELS_AVAILABLE = False
    predictor = None

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Kicks ML Prediction API',
        'models_available': MODELS_AVAILABLE,
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Health check for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'models': 'loaded' if MODELS_AVAILABLE else 'not loaded'
    }), 200 if MODELS_AVAILABLE else 503

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Get dropdown metadata for UI"""
    if not MODELS_AVAILABLE:
        return jsonify({'error': 'Model not available'}), 503

    try:
        metadata = predictor.get_metadata()
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get model performance metrics"""
    if not MODELS_AVAILABLE:
        return jsonify({'error': 'Model not available'}), 503

    try:
        metrics = predictor.get_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict demand based on input features"""
    if not MODELS_AVAILABLE:
        return jsonify({'error': 'Model not available. Please check server logs.'}), 503

    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['retailer', 'region', 'product', 'sales_method',
                          'price_per_unit', 'month', 'quarter']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Make prediction
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

    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/api/check-models', methods=['GET'])
def check_models():
    """Check if models are loaded and ready"""
    return jsonify({
        'available': MODELS_AVAILABLE,
        'message': 'Model ready for predictions' if MODELS_AVAILABLE else 'Model not loaded'
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
