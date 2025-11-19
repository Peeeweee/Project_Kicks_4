# /run.py

import sys
import os
import traceback

# Add the project root to the Python path for better import resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dashboard import create_app

    # Create the Flask app instance
    app = create_app()

except Exception as e:
    # Log the full error for debugging on Vercel
    print(f"CRITICAL ERROR: Failed to create Flask app")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print(f"Full traceback:")
    traceback.print_exc()

    # Re-raise the exception so Vercel logs it
    raise

# This is the WSGI application that Vercel will use
# Vercel automatically detects 'app' as the WSGI application
# For local development, run with: python run.py

if __name__ == '__main__':
    # Local development server
    # Using port 5001 as specified in the original app.py
    app.run(debug=True, host='0.0.0.0', port=5001)