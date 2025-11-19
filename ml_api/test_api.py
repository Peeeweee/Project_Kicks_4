"""
Test script for ML API
Run this to verify the API works before deploying
"""

import requests
import json

# Change this to your deployed URL after deployment
# For local testing: http://localhost:5000
API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_metadata():
    """Test metadata endpoint"""
    print("\n=== Testing Metadata Endpoint ===")
    response = requests.get(f"{API_URL}/api/metadata")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Retailers: {data.get('retailers', [])[:3]}...")  # Show first 3
    print(f"Regions: {data.get('regions', [])}")
    print(f"Products: {data.get('products', [])[:3]}...")

def test_metrics():
    """Test metrics endpoint"""
    print("\n=== Testing Metrics Endpoint ===")
    response = requests.get(f"{API_URL}/api/metrics")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_prediction():
    """Test prediction endpoint"""
    print("\n=== Testing Prediction Endpoint ===")

    test_data = {
        "retailer": "Foot Locker",
        "region": "West",
        "product": "Men's Street Footwear",
        "sales_method": "In-store",
        "price_per_unit": 50.0,
        "month": 6,
        "quarter": 2
    }

    print(f"Input: {json.dumps(test_data, indent=2)}")

    response = requests.post(
        f"{API_URL}/api/predict",
        json=test_data
    )

    print(f"Status Code: {response.status_code}")
    result = response.json()

    if response.status_code == 200:
        print("\n✅ Prediction Successful!")
        print(f"Predicted Units: {result.get('predicted_units', 0):.0f}")
        print(f"Predicted Revenue: ${result.get('predicted_sales', 0):,.2f}")
        print(f"Confidence Score: {result.get('confidence_score', 0):.1f}%")
        print(f"Confidence Level: {result.get('confidence_level', 'Unknown')}")
        print(f"\nUnits Range: {result.get('units_lower', 0):.0f} - {result.get('units_upper', 0):.0f}")
        print(f"Revenue Range: ${result.get('sales_lower', 0):,.2f} - ${result.get('sales_upper', 0):,.2f}")
    else:
        print(f"\n❌ Prediction Failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    print("=" * 60)
    print("ML API Test Suite")
    print("=" * 60)

    try:
        test_health()
        test_metadata()
        test_metrics()
        test_prediction()

        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print(f"Make sure the API is running at {API_URL}")
        print("\nTo start the API locally:")
        print("  cd ml_api")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
