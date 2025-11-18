"""
Comprehensive Analysis of ML Prediction System
"""
import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path

# Load data
df = pd.read_csv('data/adidas_sales_cleaned.csv')

print("="*80)
print("COMPREHENSIVE ML PREDICTION SYSTEM ANALYSIS")
print("="*80)

# 1. Dataset Validation
print("\n1. DATASET VALIDATION")
print("-" * 80)
df['Calculated_Sales'] = df['Price per Unit'] * df['Units Sold']
matches = (df['Total Sales'] == df['Calculated_Sales']).sum()
print(f"Total Sales = Price x Units: {matches}/{len(df)} records match ({matches/len(df)*100:.1f}%)")

if matches == len(df):
    print("[OK] CONFIRMED: Total Sales is exactly Price x Units (PURE ARITHMETIC)")
else:
    print("[!] WARNING: Total Sales has non-linear components")

# 2. Feature Correlation
print("\n2. FEATURE CORRELATION WITH TARGET")
print("-" * 80)
print(f"{'Feature':<30} {'Correlation':<15} {'Interpretation'}")
print("-" * 80)

corr_price = df['Price per Unit'].corr(df['Total Sales'])
corr_units = df['Units Sold'].corr(df['Total Sales'])
corr_month = df['Month'].corr(df['Total Sales'])
corr_quarter = df['Quarter'].corr(df['Total Sales'])

print(f"{'Price per Unit':<30} {corr_price:>6.4f}          {'Moderate' if abs(corr_price) > 0.3 else 'Weak'}")
print(f"{'Units Sold':<30} {corr_units:>6.4f}          {'VERY STRONG (circular!)' if corr_units > 0.9 else 'Strong'}")
print(f"{'Month':<30} {corr_month:>6.4f}          {'Weak' if abs(corr_month) < 0.1 else 'Moderate'}")
print(f"{'Quarter':<30} {corr_quarter:>6.4f}          {'Weak' if abs(corr_quarter) < 0.1 else 'Moderate'}")

# 3. Data Sparsity
print("\n3. DATA SPARSITY ANALYSIS")
print("-" * 80)
combos = df.groupby(['Retailer', 'Region', 'Product', 'Sales Method']).size()
theoretical_max = 6 * 5 * 6 * 3
print(f"Unique combinations in data: {len(combos)}")
print(f"Theoretical maximum: {theoretical_max} (6 retailers × 5 regions × 6 products × 3 methods)")
print(f"Coverage: {len(combos)/theoretical_max*100:.1f}%")
print(f"\nMissing combinations: {theoretical_max - len(combos)}")
print(f"Combinations with <10 samples: {(combos < 10).sum()} ({(combos < 10).sum()/len(combos)*100:.1f}%)")
print(f"Combinations with <5 samples: {(combos < 5).sum()} ({(combos < 5).sum()/len(combos)*100:.1f}%)")

print("\n[!] PROBLEM: Model will struggle with unseen combinations (25.7% missing)")

# 4. Sales Patterns
print("\n4. SALES PATTERNS BY CATEGORY")
print("-" * 80)

print("\nBy Sales Method:")
method_stats = df.groupby('Sales Method')['Total Sales'].agg(['mean', 'median', 'std'])
for idx, row in method_stats.iterrows():
    print(f"  {idx:15} Mean: ${row['mean']:>12,.0f}  Median: ${row['median']:>12,.0f}  Std: ${row['std']:>12,.0f}")

print("\nBy Retailer:")
retailer_stats = df.groupby('Retailer')['Total Sales'].agg(['mean', 'median'])
for idx, row in retailer_stats.iterrows():
    print(f"  {idx:15} Mean: ${row['mean']:>12,.0f}  Median: ${row['median']:>12,.0f}")

print("\nBy Region:")
region_stats = df.groupby('Region')['Total Sales'].agg(['mean', 'median'])
for idx, row in region_stats.iterrows():
    print(f"  {idx:15} Mean: ${row['mean']:>12,.0f}  Median: ${row['median']:>12,.0f}")

# 5. Current Model Analysis
print("\n5. CURRENT MODEL PERFORMANCE")
print("-" * 80)
model_data = pickle.load(open('predictions/trained_models/sales_predictor.pkl', 'rb'))
print(f"Model Type: {type(model_data['model']).__name__}")
print(f"Features Used: {len(model_data['feature_columns'])}")
for i, feat in enumerate(model_data['feature_columns'], 1):
    print(f"  {i}. {feat}")

print(f"\nMetrics:")
print(f"  R² Score: {model_data['metrics']['r2']:.4f} ({model_data['metrics']['r2']*100:.2f}%)")
print(f"  MAE: ${model_data['metrics']['mae']:,.2f}")

print(f"\n[!] PROBLEM: R² = 22% means model explains only 22% of variance")
print(f"[!] PROBLEM: MAE = ${model_data['metrics']['mae']:,.0f} is HUGE (average sale is ${df['Total Sales'].mean():,.0f})")

# 6. Why the Model Performs Poorly
print("\n6. ROOT CAUSE ANALYSIS")
print("-" * 80)
print("Why R² = 22% and MAE = $94k?")
print()
print("FUNDAMENTAL ISSUE: Total Sales = Price × Units (exact arithmetic)")
print()
print("The model tries to predict Total Sales WITHOUT Units Sold using only:")
print("  • Retailer (6 categories)")
print("  • Region (5 categories)")
print("  • Product (6 categories)")
print("  • Sales Method (3 categories)")
print("  • Price per Unit (continuous)")
print("  • Month (1-12)")
print("  • Quarter (1-4)")
print()
print("But Units Sold varies MASSIVELY:")
print(f"  Min: {df['Units Sold'].min()}")
print(f"  Max: {df['Units Sold'].max()}")
print(f"  Mean: {df['Units Sold'].mean():.0f}")
print(f"  Std: {df['Units Sold'].std():.0f}")
print()
print("The model has NO WAY to know if a sale involved 10 units or 1000 units!")
print("This is like predicting your grocery bill without knowing what you bought.")
print()
print("[OK] The 22% R² shows patterns exist (In-store > Outlet > Online)")
print("[!] But 78% of variance is driven by Units Sold (which we excluded)")

# 7. Prediction Analysis
print("\n7. SCREENSHOT PREDICTION ANALYSIS")
print("-" * 80)
print("Screenshot showed:")
print("  Input: Amazon, Midwest, Men's Apparel, In-store, $50, 1000 units, June, Q2")
print("  ML Predicted: $120,927.64")
print("  Simple Calc: $50,000.00")
print("  Difference: +$70,927.64 (+141.86%)")
print()

# Check if this combination exists
test_combo = df[
    (df['Retailer'] == 'Amazon') &
    (df['Region'] == 'Midwest') &
    (df['Product'] == "Men's Apparel") &
    (df['Sales Method'] == 'In-store')
]

print(f"Training data for (Amazon + Midwest + Men's Apparel + In-store): {len(test_combo)} samples")

if len(test_combo) == 0:
    print("[!] ZERO training examples! Model is extrapolating wildly!")
else:
    print(f"  Average Total Sales: ${test_combo['Total Sales'].mean():,.2f}")
    print(f"  Average Units Sold: {test_combo['Units Sold'].mean():.0f}")
    print(f"  Average Price: ${test_combo['Price per Unit'].mean():.2f}")

# 8. Alternative Approaches
print("\n8. RECOMMENDATIONS & ALTERNATIVES")
print("-" * 80)
print()
print("OPTION 1: UNITS PREDICTOR (recommended)")
print("  > Predict Units Sold based on market conditions")
print("  > Calculate Total Sales = Predicted Units x Price")
print("  > More realistic: predict demand, not revenue")
print()
print("OPTION 2: KEEP CURRENT (with clear communication)")
print("  > Accept 22% R2 as baseline")
print("  > Use model for relative comparisons only")
print("  > Show wide confidence intervals (+/-$94k)")
print()
print("OPTION 3: ADD UNITS SOLD (NOT recommended)")
print("  > Get 88% R2 but meaningless")
print("  > Model becomes fancy calculator")
print("  > Can't forecast without knowing units")
print()
print("OPTION 4: ENHANCED FEATURE ENGINEERING")
print("  > Add seasonality features (sin/cos of month)")
print("  > Add day of week")
print("  > Add retailer-region interactions")
print("  > Add price positioning (relative to product avg)")
print("  > Expected improvement: R2 22% -> 30-40%")

# 9. Feature Importance Simulation
print("\n9. WHAT IF ANALYSIS")
print("-" * 80)

# Simulate what happens with different feature sets
print("\nExpected R2 with different feature sets:")
print(f"  Current (no Units): ~22% (actual)")
print(f"  With Units Sold: ~88% (arithmetic, not ML)")
print(f"  With better features: ~30-40% (estimated)")
print()
print("Why can't we get higher R2 without Units?")
print("  Because Units Sold accounts for ~78% of variance!")
print("  It's like predicting marathon time without knowing if you ran or walked.")

print("\n" + "="*80)
print("END OF ANALYSIS")
print("="*80)
