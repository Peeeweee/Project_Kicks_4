"""
ML Predictions Setup Script

This script helps you set up and test the ML predictions feature.
"""

import subprocess
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*80)
    print(text)
    print("="*80)

def check_dependencies():
    """Check if required packages are installed"""
    print_header("CHECKING DEPENDENCIES")

    required = ['pandas', 'numpy', 'sklearn', 'flask']
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} is NOT installed")

    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        return False

    print("\n✓ All dependencies installed!")
    return True

def train_models():
    """Train the ML models"""
    print_header("TRAINING MODELS")

    train_script = Path(__file__).parent / "predictions" / "train_models.py"

    if not train_script.exists():
        print("✗ Training script not found!")
        return False

    print("Running training script...")
    print("This will take about 30 seconds...\n")

    try:
        result = subprocess.run(
            [sys.executable, str(train_script)],
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print("\n✓ Models trained successfully!")
            return True
        else:
            print(f"\n✗ Training failed with code {result.returncode}")
            return False

    except Exception as e:
        print(f"\n✗ Error during training: {e}")
        return False

def check_models_exist():
    """Check if trained models exist"""
    print_header("CHECKING TRAINED MODELS")

    models_dir = Path(__file__).parent / "predictions" / "trained_models"

    if not models_dir.exists():
        print("✗ Models directory does not exist")
        return False

    required_files = [
        "sales_predictor.pkl",
        "category_classifier.pkl",
        "product_recommender.pkl",
        "metadata.json"
    ]

    all_exist = True
    for filename in required_files:
        filepath = models_dir / filename
        if filepath.exists():
            print(f"✓ {filename} found")
        else:
            print(f"✗ {filename} NOT found")
            all_exist = False

    if all_exist:
        print("\n✓ All model files present!")
    else:
        print("\n⚠ Some model files are missing")

    return all_exist

def print_instructions():
    """Print instructions for using the predictions"""
    print_header("HOW TO USE ML PREDICTIONS")

    print("""
📊 Your ML prediction system is ready!

To use it:

1. Start the Flask dashboard:

   python run.py

2. Open your browser and navigate to:

   http://localhost:5001/ml-prediction

3. You'll see 3 prediction tools:

   💰 Sales Amount Predictor - Forecast revenue
   🏷️ Sales Category Classifier - Classify high/medium/low
   📦 Product Recommender - Get product suggestions

4. Fill in the forms and click the predict buttons!

Tips:
- Experiment with different input values
- Compare predictions with expected results
- Use for real business decisions

For more information, see:
- predictions/README.md
- ml_model/SIMPLE_MODELS_QUICKSTART.md
""")

def main():
    """Main setup flow"""
    print_header("ML PREDICTIONS SETUP")
    print("This script will help you set up the ML predictions feature\n")

    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)

    # Step 2: Check if models already exist
    models_exist = check_models_exist()

    if models_exist:
        print("\n✅ Models already trained!")
        response = input("\nDo you want to retrain the models? (y/n): ")
        if response.lower() != 'y':
            print_instructions()
            return

    # Step 3: Train models
    if not models_exist or response.lower() == 'y':
        success = train_models()
        if not success:
            print("\n❌ Setup failed during training")
            sys.exit(1)

    # Step 4: Verify everything is ready
    print_header("FINAL CHECK")

    if check_models_exist():
        print("\n" + "="*80)
        print("✅ SETUP COMPLETE!")
        print("="*80)
        print_instructions()
    else:
        print("\n❌ Setup incomplete - please check errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()
