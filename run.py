# /run.py

from dashboard import create_app

# Create the Flask app instance
app = create_app()

# This is the WSGI application that Vercel will use
# Vercel automatically detects 'app' as the WSGI application
# For local development, run with: python run.py

if __name__ == '__main__':
    # Local development server
    # Using port 5001 as specified in the original app.py
    app.run(debug=True, host='0.0.0.0', port=5001)