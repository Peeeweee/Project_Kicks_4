"""
Prediction Service for Dashboard

This module provides demand forecasting using the trained Units Predictor model.
Predicts Units Sold, then calculates Total Sales = Units × Price
"""

import pickle
import numpy as np
from pathlib import Path
import json

MODEL_DIR = Path(__file__).parent / "trained_models"

class UnitsPredictor:
    """Units prediction service for demand forecasting"""

    def __init__(self):
        self.units_model = None
        self.metadata = None
        self.load_models()

    def load_models(self):
        """Load trained Units Predictor model"""
        try:
            # Load units predictor
            with open(MODEL_DIR / "units_predictor.pkl", 'rb') as f:
                self.units_model = pickle.load(f)

            # Load metadata
            with open(MODEL_DIR / "metadata.json", 'r') as f:
                self.metadata = json.load(f)

            return True

        except FileNotFoundError:
            return False

    def models_exist(self):
        """Check if model is loaded"""
        return self.units_model is not None

    def predict_demand(self, retailer, region, product, sales_method,
                      price_per_unit, month, quarter):
        """
        Predict Units Sold (demand forecasting) and calculate Total Sales with confidence intervals

        Args:
            retailer: Retailer name (e.g., 'Foot Locker')
            region: Region name (e.g., 'Northeast')
            product: Product name (e.g., 'Men\'s Athletic Footwear')
            sales_method: Sales method (e.g., 'In-store')
            price_per_unit: Price per unit (float)
            month: Month number (1-12)
            quarter: Quarter number (1-4)

        Returns:
            dict with units prediction, calculated sales, confidence intervals, and metrics
        """
        if not self.units_model:
            return {'error': 'Model not loaded'}

        try:
            # Encode categorical features
            features = []
            encoders = self.units_model['encoders']

            for col, value in [('Retailer', retailer), ('Region', region),
                              ('Product', product), ('Sales Method', sales_method)]:
                encoded = encoders[col].transform([value])[0]
                features.append(encoded)

            # Add numerical features
            features.extend([
                float(price_per_unit),
                int(month),
                int(quarter)
            ])

            # Make prediction for Units Sold
            X_pred = np.array(features).reshape(1, -1)
            predicted_units = self.units_model['model'].predict(X_pred)[0]

            # Ensure non-negative units
            predicted_units = max(0, predicted_units)

            # Calculate confidence intervals
            # Use MAE to estimate prediction uncertainty (95% confidence ~ 1.96 * MAE)
            units_mae = self.units_model['metrics']['units_mae']
            confidence_multiplier = 1.96  # 95% confidence interval

            units_margin = units_mae * confidence_multiplier
            units_lower = max(0, predicted_units - units_margin)
            units_upper = predicted_units + units_margin

            # Calculate confidence percentage (inverse of coefficient of variation)
            # Higher confidence when prediction is large relative to MAE
            units_cv = units_mae / max(predicted_units, 1)  # Avoid division by zero
            confidence_score = max(0, min(100, 100 * (1 - min(units_cv, 1))))

            # Calculate Total Sales = Units × Price
            predicted_sales = predicted_units * price_per_unit
            sales_lower = units_lower * price_per_unit
            sales_upper = units_upper * price_per_unit

            # Calculate revenue confidence interval
            revenue_mae = self.units_model['metrics']['revenue_mae']
            revenue_margin = revenue_mae * confidence_multiplier

            # Determine confidence level (High/Medium/Low)
            if confidence_score >= 75:
                confidence_level = 'High'
            elif confidence_score >= 50:
                confidence_level = 'Medium'
            else:
                confidence_level = 'Low'

            return {
                'predicted_units': float(predicted_units),
                'predicted_sales': float(predicted_sales),
                'price_per_unit': float(price_per_unit),

                # Confidence intervals
                'units_lower': float(units_lower),
                'units_upper': float(units_upper),
                'units_margin': float(units_margin),
                'sales_lower': float(sales_lower),
                'sales_upper': float(sales_upper),
                'sales_margin': float(revenue_margin),

                # Confidence metrics
                'confidence_score': float(confidence_score),
                'confidence_level': confidence_level,

                # Model metrics (for reference)
                'model_type': self.units_model['model_type'],
                'units_r2': self.units_model['metrics']['units_r2'],
                'units_mae': self.units_model['metrics']['units_mae'],
                'revenue_r2': self.units_model['metrics']['revenue_r2'],
                'revenue_mae': self.units_model['metrics']['revenue_mae']
            }

        except Exception as e:
            return {'error': str(e)}

    def get_metadata(self):
        """Get metadata for dropdown options"""
        return self.metadata

    def get_metrics(self):
        """Get model performance metrics"""
        if self.units_model and 'metrics' in self.units_model:
            return self.units_model['metrics']
        return None

# Create singleton instance
predictor = UnitsPredictor()
