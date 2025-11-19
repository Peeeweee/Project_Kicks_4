# ML Prediction API

Standalone Flask API for Adidas Sales ML predictions. Deploy this separately from the main dashboard.

## Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

1. Create a new account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: kicks-ml-api
   - **Root Directory**: ml_api
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. Add environment variable:
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0`
6. Click "Create Web Service"
7. Copy the deployment URL (e.g., `https://kicks-ml-api.onrender.com`)

### Option 2: Railway

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root Directory**: ml_api
   - Railway will auto-detect Python and use Procfile
5. Copy the deployment URL

### Option 3: Heroku

```bash
cd ml_api
heroku create kicks-ml-api
git subtree push --prefix ml_api heroku main
```

## API Endpoints

- `GET /` - Health check and service info
- `GET /health` - Health status
- `GET /api/metadata` - Get dropdown options for UI
- `GET /api/metrics` - Get model performance metrics
- `POST /api/predict` - Make predictions
- `GET /api/check-models` - Check model availability

## Testing Locally

```bash
cd ml_api
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Integration with Vercel Dashboard

After deployment, update the Vercel dashboard environment variable:
- Variable: `ML_API_URL`
- Value: Your deployed API URL (e.g., `https://kicks-ml-api.onrender.com`)
