# Deployment Guide - Kicks Analytics Dashboard

This guide explains how to deploy the dashboard with ML predictions using a split architecture:
- **Frontend + Visualizations**: Vercel (serverless)
- **ML Predictions API**: Render/Railway (handles large model files)

## Architecture

```
┌─────────────────────────────────────────────┐
│           Vercel (Frontend)                 │
│  - Dashboard UI                             │
│  - 20+ Interactive Charts                   │
│  - Data Visualizations                      │
└─────────────────┬───────────────────────────┘
                  │ HTTP Requests
                  │ (ML Predictions)
                  ▼
┌─────────────────────────────────────────────┐
│        Render/Railway (ML API)              │
│  - Random Forest Model (63 MB)              │
│  - Prediction Engine                        │
│  - Confidence Intervals                     │
└─────────────────────────────────────────────┘
```

---

## Step 1: Deploy ML API to Render (Free)

### 1.1 Push to GitHub

First, ensure all your code is committed:

```bash
git add .
git commit -m "Add ML API backend for deployment"
git push origin main
```

### 1.2 Deploy to Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `Project_Kicks` repository
5. Configure the service:

   **Service Details:**
   - **Name**: `kicks-ml-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `ml_api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

   **Plan:**
   - Select **Free** plan (512 MB RAM, spins down after 15 min inactivity)

6. Click **"Create Web Service"**

7. Wait for deployment (5-10 minutes)

8. **Copy your ML API URL** (e.g., `https://kicks-ml-api.onrender.com`)

### 1.3 Test ML API

Visit your API URL to verify it's working:
- `https://kicks-ml-api.onrender.com/` - Should show API status
- `https://kicks-ml-api.onrender.com/health` - Health check
- `https://kicks-ml-api.onrender.com/api/check-models` - Model status

---

## Step 2: Deploy Dashboard to Vercel

### 2.1 Verify .vercelignore Configuration

The `.vercelignore` file excludes the ML-related folders since they're not needed on Vercel:

Your `.vercelignore` should include:
```
predictions/        # Entire ML prediction module (handled by external API)
ml_api/            # ML API code (deployed separately to Render)
```

**Note**: The `data/` folder with the CSV file IS included in deployment (needed for dashboard charts).

This prevents the 63 MB model and ML dependencies from being uploaded to Vercel, keeping the deployment under 250 MB. ✅ Already configured!

### 2.2 Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New..."** → **"Project"**
3. Import your `Project_Kicks` repository
4. Configure:

   **Framework Preset**: Other
   **Root Directory**: `./` (leave as is)
   **Build Command**: (leave empty)
   **Output Directory**: (leave empty)

5. **Add Environment Variable**:
   - **Name**: `ML_API_URL`
   - **Value**: `https://kicks-ml-api.onrender.com` (your Render URL)

6. Click **"Deploy"**

7. Wait for deployment (2-3 minutes)

8. Your dashboard will be live at: `https://project-kicks-your-username.vercel.app`

---

## Step 3: Verify Everything Works

### 3.1 Test Dashboard
1. Visit your Vercel URL
2. Navigate through all pages:
   - ✅ Sales Dashboard
   - ✅ Product Analysis
   - ✅ Customer Insights
   - ✅ About Page

### 3.2 Test ML Predictions
1. Go to ML Prediction page
2. Fill out the form:
   - Retailer: Any option
   - Region: Any option
   - Product: Any option
   - Sales Method: Any option
   - Price: e.g., 50
   - Month: e.g., 6
   - Quarter: e.g., 2
3. Click **"Predict Demand"**
4. Should see:
   - ✅ Predicted units
   - ✅ Predicted revenue
   - ✅ Confidence intervals
   - ✅ Confidence score

---

## Troubleshooting

### ML API shows "Model not loaded"

**Check Render logs:**
1. Go to Render dashboard → Your service
2. Click "Logs" tab
3. Look for errors during startup

**Common fixes:**
- Ensure `predictions/` folder is in the repo root
- Check that `predictions/trained_models/units_predictor.pkl` exists
- Verify Python version compatibility

### Dashboard can't connect to ML API

**Check environment variable:**
1. Go to Vercel → Project Settings → Environment Variables
2. Verify `ML_API_URL` is set correctly
3. Must be: `https://kicks-ml-api.onrender.com` (no trailing slash)

**Test API directly:**
```bash
curl https://kicks-ml-api.onrender.com/health
```

Should return: `{"status":"healthy","models":"loaded"}`

### Render service is sleeping (Free tier)

Free tier spins down after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

**Solutions:**
1. **Keep-alive service**: Use a free cron job to ping your API every 10 minutes
2. **Upgrade to paid**: $7/month for always-on service
3. **Accept cold starts**: First user waits 30s, then fast for 15 min

---

## Cost Summary

| Service | Plan | Cost | Features |
|---------|------|------|----------|
| **Vercel** | Hobby | **FREE** | Dashboard, 100GB bandwidth, serverless |
| **Render** | Free | **FREE** | ML API, 512MB RAM, sleeps after 15min |
| **Total** | | **$0/month** | Full ML functionality! |

---

## Alternative: Local Development

If you prefer running everything locally:

```bash
# Terminal 1: Start dashboard
python run.py

# Terminal 2: Start ML API (optional for testing)
cd ml_api
python app.py
```

Set local environment variable:
```bash
export ML_API_URL=http://localhost:5000
```

---

## Production Recommendations

For production deployments with high traffic:

1. **Render Paid Plan** ($7/mo)
   - Always-on (no cold starts)
   - More RAM for faster predictions

2. **Railway** (Similar to Render)
   - $5/month for 500 hours
   - Better uptime

3. **AWS/GCP** (Advanced)
   - Deploy ML API on Lambda/Cloud Functions
   - Use S3/Cloud Storage for model files
   - Higher cost but unlimited scale

---

## Success! 🎉

Your Adidas Sales Analytics Dashboard is now live with:
- ✅ 20+ Interactive visualizations
- ✅ Real-time filtering and data exploration
- ✅ ML-powered demand forecasting with 82.8% accuracy
- ✅ Dynamic confidence intervals
- ✅ Professional UI with Bootstrap 5
- ✅ Completely free hosting!

**Share your dashboard:**
- Production: `https://your-app.vercel.app`
- ML API: `https://kicks-ml-api.onrender.com`
