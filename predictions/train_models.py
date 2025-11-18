"""
Train Units Predictor Model for Adidas Sales

This script trains a demand forecasting model:
- Units Predictor (Linear Regression) - Predicts Units Sold
- Total Sales is calculated as: Predicted Units x Price per Unit
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import json
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

# File paths
DATA_FILE = Path(__file__).parent.parent / "data" / "adidas_sales_cleaned.csv"
MODEL_DIR = Path(__file__).parent / "trained_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

def print_header(text):
    print("\n" + "="*80)
    print(text)
    print("="*80)

def train_units_predictor(df):
    """Train model to predict Units Sold (demand forecasting)"""
    print_header("TRAINING UNITS PREDICTOR (DEMAND FORECASTING)")

    print("\n[INFO] Target: Units Sold")
    print("[INFO] Approach: Predict demand, then calculate revenue = Units x Price")
    print("[INFO] This solves the circular dependency problem!\n")

    # Prepare features (WITHOUT Units Sold, WITHOUT Total Sales)
    # We predict Units Sold based on market conditions
    features_to_use = ['Retailer', 'Region', 'Product', 'Sales Method',
                       'Price per Unit', 'Month', 'Quarter']

    df_model = df[features_to_use + ['Units Sold']].copy()

    # Encode categorical variables
    label_encoders = {}
    categorical_cols = ['Retailer', 'Region', 'Product', 'Sales Method']

    for col in categorical_cols:
        le = LabelEncoder()
        df_model[col + '_encoded'] = le.fit_transform(df_model[col])
        label_encoders[col] = le

    # Prepare X and y
    feature_columns = [col + '_encoded' for col in categorical_cols] + \
                     ['Price per Unit', 'Month', 'Quarter']

    X = df_model[feature_columns].values
    y = df_model['Units Sold'].values

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    print(f"Training samples: {len(X_train):,}")
    print(f"Test samples: {len(X_test):,}")
    print(f"\nUnits Sold statistics:")
    print(f"  Min: {df['Units Sold'].min()}")
    print(f"  Max: {df['Units Sold'].max()}")
    print(f"  Mean: {df['Units Sold'].mean():.0f}")
    print(f"  Median: {df['Units Sold'].median():.0f}")
    print(f"  Std: {df['Units Sold'].std():.0f}")

    # Train Linear Regression model
    print("\n[TRAINING] Linear Regression model...")
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)

    y_pred_lr = model_lr.predict(X_test)
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    r2_lr = r2_score(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))

    print(f"  MAE: {mae_lr:.2f} units")
    print(f"  RMSE: {rmse_lr:.2f} units")
    print(f"  R2: {r2_lr:.4f} ({r2_lr*100:.2f}%)")

    # Train Random Forest for comparison
    print("\n[TRAINING] Random Forest model (for comparison)...")
    model_rf = RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
    model_rf.fit(X_train, y_train)

    y_pred_rf = model_rf.predict(X_test)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    r2_rf = r2_score(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

    print(f"  MAE: {mae_rf:.2f} units")
    print(f"  RMSE: {rmse_rf:.2f} units")
    print(f"  R2: {r2_rf:.4f} ({r2_rf*100:.2f}%)")

    # Choose best model
    if r2_rf > r2_lr:
        print(f"\n[DECISION] Using Random Forest (R2: {r2_rf:.4f} > {r2_lr:.4f})")
        model = model_rf
        mae = mae_rf
        r2 = r2_rf
        rmse = rmse_rf
        model_type = 'RandomForest'
    else:
        print(f"\n[DECISION] Using Linear Regression (R2: {r2_lr:.4f} >= {r2_rf:.4f})")
        model = model_lr
        mae = mae_lr
        r2 = r2_lr
        rmse = rmse_lr
        model_type = 'LinearRegression'

    # Validate: Calculate revenue and compare to actual Total Sales
    print("\n" + "-"*80)
    print("REVENUE VALIDATION")
    print("-"*80)

    # FIXED: Properly align test data with predictions
    # Since we use train_test_split with random_state, we need to track the actual test data

    # Create a combined dataframe for splitting that includes Price and Units
    split_data = df_model[feature_columns].copy()
    split_data['Price per Unit'] = df_model['Price per Unit']
    split_data['Units Sold'] = df_model['Units Sold']

    # Split with same random_state to get matching indices
    _, test_data, _, _ = train_test_split(
        split_data,
        df_model['Units Sold'],
        test_size=0.2,
        random_state=RANDOM_STATE
    )

    # Get actual prices and units from the test set
    prices_test = test_data['Price per Unit'].values
    actual_units_test = test_data['Units Sold'].values
    actual_sales = actual_units_test * prices_test  # Actual revenue

    # Calculate predicted revenue
    predicted_units = model.predict(X_test)
    predicted_revenue = predicted_units * prices_test

    # Calculate revenue metrics
    revenue_mae = mean_absolute_error(actual_sales, predicted_revenue)
    revenue_r2 = r2_score(actual_sales, predicted_revenue)
    revenue_rmse = np.sqrt(mean_squared_error(actual_sales, predicted_revenue))

    print(f"\nRevenue MAE: ${revenue_mae:,.2f}")
    print(f"Revenue RMSE: ${revenue_rmse:,.2f}")
    print(f"Revenue R2 Score: {revenue_r2:.4f} ({revenue_r2*100:.2f}%)")

    # Sample predictions
    print("\n" + "-"*80)
    print("SAMPLE PREDICTIONS (first 5 test samples)")
    print("-"*80)
    print(f"{'Actual Units':>12} {'Pred Units':>12} {'Price':>8} {'Actual Revenue':>15} {'Pred Revenue':>15} {'Error':>12}")
    print("-"*80)

    for i in range(min(5, len(predicted_units))):
        actual_u = actual_units_test[i]
        pred_u = predicted_units[i]
        price = prices_test[i]
        actual_r = actual_sales[i]
        pred_r = predicted_revenue[i]
        error = pred_r - actual_r

        print(f"{actual_u:>12.0f} {pred_u:>12.0f} ${price:>7.2f} ${actual_r:>14,.2f} ${pred_r:>14,.2f} ${error:>11,.2f}")

    print("-"*80)

    # Save model
    model_data = {
        'model': model,
        'model_type': model_type,
        'encoders': label_encoders,
        'feature_columns': feature_columns,
        'categorical_cols': categorical_cols,
        'metrics': {
            'units_mae': mae,
            'units_rmse': rmse,
            'units_r2': r2,
            'revenue_mae': revenue_mae,
            'revenue_rmse': revenue_rmse,
            'revenue_r2': revenue_r2,
        },
        'trained_date': datetime.now().isoformat(),
        'description': 'Units Predictor - Predicts Units Sold, then calculates Total Sales = Units x Price'
    }

    model_path = MODEL_DIR / "units_predictor.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)

    print(f"\n[OK] Model saved to: {model_path}")

    return model_data

def save_metadata(df):
    """Save metadata about unique values for dropdowns"""
    print_header("SAVING METADATA")

    metadata = {
        'retailers': sorted(df['Retailer'].unique().tolist()),
        'regions': sorted(df['Region'].unique().tolist()),
        'products': sorted(df['Product'].unique().tolist()),
        'sales_methods': sorted(df['Sales Method'].unique().tolist()),
        'months': ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'],
        'quarters': [1, 2, 3, 4],
        'price_range': {
            'min': float(df['Price per Unit'].min()),
            'max': float(df['Price per Unit'].max()),
            'avg': float(df['Price per Unit'].mean())
        },
        'units_range': {
            'min': int(df['Units Sold'].min()),
            'max': int(df['Units Sold'].max()),
            'avg': float(df['Units Sold'].mean()),
            'median': float(df['Units Sold'].median())
        }
    }

    metadata_path = MODEL_DIR / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"[OK] Metadata saved to: {metadata_path}")

def main():
    """Main training pipeline"""
    print_header("ADIDAS UNITS PREDICTOR - DEMAND FORECASTING")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load data
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
    print(f"[OK] Loaded {len(df):,} records\n")

    # Train model
    model = train_units_predictor(df)

    # Save metadata
    save_metadata(df)

    print_header("TRAINING COMPLETE")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("[SUCCESS] Units Predictor trained successfully!")
    print(f"\nModel Type: {model['model_type']}")
    print(f"Units R2: {model['metrics']['units_r2']:.4f} ({model['metrics']['units_r2']*100:.2f}%)")
    print(f"Units MAE: {model['metrics']['units_mae']:.2f} units")
    print(f"Revenue R2: {model['metrics']['revenue_r2']:.4f} ({model['metrics']['revenue_r2']*100:.2f}%)")
    print(f"Revenue MAE: ${model['metrics']['revenue_mae']:,.2f}")

    print(f"\nModel saved to: {MODEL_DIR}\n")
    print("Files:")
    print("  1. units_predictor.pkl - Predicts Units Sold (demand)")
    print("  2. metadata.json - Dropdown values for UI")
    print("\nHow it works:")
    print("  1. Model predicts Units Sold based on market conditions")
    print("  2. Revenue calculated as: Predicted Units x Price per Unit")
    print("  3. No circular dependency - true demand forecasting!")
    print("\nReady to use in the dashboard!")

if __name__ == "__main__":
    main()
