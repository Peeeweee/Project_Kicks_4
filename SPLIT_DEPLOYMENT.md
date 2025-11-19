# Split Architecture Deployment Guide

Since the all-in-one deployment exceeded Vercel's 250 MB limit, we're using a **split architecture**:

- **Vercel**: Dashboard (charts, UI) - ~30 MB
- **Render**: ML API (model, predictions) - ~50 MB

---

## 🎯 Quick Deploy

### Step 1: Deploy Dashboard to Vercel

```bash
# Commit changes
git add .
git commit -m "Configure split deployment"
git push origin main
```

Then on Vercel:
1. Go to https://vercel.com
2. Import your GitHub repository
3. **No environment variables needed yet**
4. Click "Deploy"

**Dashboard will be live but ML predictions won't work yet** (needs ML API URL)

---

### Step 2: Deploy ML API to Render

1. Go to https://render.com
2. Create new account (free)
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Configure:
   - **Name**: `kicks-ml-api`
   - **Root Directory**: `ml_api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

6. Click "Create Web Service"

Wait for deployment (~5-10 minutes). You'll get a URL like:
```
https://kicks-ml-api.onrender.com
```

**Test the API:**
```bash
curl https://kicks-ml-api.onrender.com/api/check-models
```

Should return:
```json
{
  "available": true,
  "message": "Model ready"
}
```

---

### Step 3: Connect Dashboard to ML API

1. Go to Vercel dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Key**: `ML_API_URL`
   - **Value**: `https://kicks-ml-api.onrender.com` (your Render URL)
   - **Environment**: Production

5. Go to **Deployments**
6. Click "Redeploy" on latest deployment

**Now everything should work!** 🎉

---

## 📁 What Changed

### Files Modified:

1. **requirements-vercel.txt** (NEW)
   - Lightweight dependencies without scikit-learn/numpy
   - Used by Vercel deployment

2. **vercel.json**
   - Now uses `requirements-vercel.txt` instead of `requirements.txt`
   - Reduces deployment size

3. **.vercelignore**
   - Now excludes `predictions/` folder
   - ML model not deployed to Vercel

4. **dashboard/pages/ml_prediction/routes.py**
   - Auto-detects `ML_API_URL` environment variable
   - Falls back to local predictor if not set
   - Forwards requests to external API when configured

### Files Unchanged:

- `ml_api/` - Ready for Render deployment
- `predictions/` - Still works locally
- All other dashboard code

---

## 🔄 How It Works

### Local Development (No ML_API_URL)
```
Browser → Flask (localhost:5001) → Local Predictor → Model
```

### Production (With ML_API_URL)
```
Browser → Vercel Dashboard → Render ML API → Model
```

**Automatic switching based on `ML_API_URL` environment variable!**

---

## 🐛 Troubleshooting

### Dashboard deployed but ML predictions fail

**Check:**
1. Render ML API is running
2. `ML_API_URL` environment variable is set on Vercel
3. Redeploy Vercel after adding environment variable

**Test ML API:**
```bash
curl https://YOUR-RENDER-URL.onrender.com/api/check-models
```

### Render API returns "Application failed to respond"

**Common causes:**
1. First request after inactivity (cold start ~30-60 seconds on free tier)
2. ML model loading (first boot takes longer)
3. Just wait and refresh

### Month dropdown still shows numbers

- Hard refresh browser: `Ctrl + Shift + R`
- Clear browser cache

---

## 💰 Cost

### Vercel (Dashboard)
- **Free Tier**: 100 GB bandwidth/month
- **Cost**: $0/month ✅

### Render (ML API)
- **Free Tier**: 750 hours/month
- **Limitations**: Spins down after 15 minutes of inactivity
- **Cold start**: 30-60 seconds for first request
- **Cost**: $0/month ✅

**Total Cost: $0/month** 🎉

### Upgrade Options (Optional)

If you need faster response times:
- **Render Starter**: $7/month - No spin-down, always active

---

## 🎯 Testing Checklist

After deployment, test:

### Dashboard (Vercel)
- [ ] Sales Overview page loads
- [ ] Product Analysis page loads
- [ ] Customer Patterns page loads
- [ ] About page loads
- [ ] Charts render correctly

### ML Predictions (Render + Vercel)
- [ ] ML Predictions page loads
- [ ] Month dropdown shows names (January, February, etc.)
- [ ] Form has all dropdowns populated
- [ ] Make a test prediction
- [ ] Results display correctly
- [ ] Confidence intervals show
- [ ] Model metrics display

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────┐
│   User Browser                  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Vercel (Dashboard)            │
│   • Flask routes                │
│   • Charts (Plotly)             │
│   • Data (1.3 MB CSV)           │
│   • Templates                   │
│   Size: ~30 MB                  │
└────────────┬────────────────────┘
             │
             │ ML_API_URL env var
             │ (only for /ml-prediction)
             ▼
┌─────────────────────────────────┐
│   Render (ML API)               │
│   • Flask API                   │
│   • Random Forest Model (24 MB) │
│   • Predictor service           │
│   • scikit-learn, numpy         │
│   Size: ~50 MB                  │
└─────────────────────────────────┘
```

---

## 🔗 Deployment URLs

After deployment, you'll have:

1. **Dashboard**: `https://your-project.vercel.app`
2. **ML API**: `https://kicks-ml-api.onrender.com`

Set `ML_API_URL` on Vercel to connect them.

---

## 📝 Next Steps

1. ✅ Deploy dashboard to Vercel
2. ✅ Deploy ML API to Render
3. ✅ Add `ML_API_URL` environment variable on Vercel
4. ✅ Redeploy Vercel
5. ✅ Test all features
6. 🎯 Add custom domain (optional)
7. 🎯 Monitor usage and performance

---

**Ready to deploy!** Follow the steps above to get your dashboard live. 🚀

For detailed instructions on Render deployment, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
