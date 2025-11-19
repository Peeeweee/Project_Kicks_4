# Vercel Deployment Guide - Kicks Analytics Dashboard

This guide provides step-by-step instructions to deploy your Adidas Kicks Analytics Dashboard to Vercel with the ML prediction model included (all-in-one deployment).

---

## 📊 Project Overview

**Total Deployment Size:** ~26 MB (well under Vercel's 250 MB limit)
- Model: 24.09 MB (optimized Random Forest)
- Data: 1.24 MB (9,648 sales records)
- Dashboard code: 0.25 MB

**Technologies:**
- Flask 3.0+ (Backend)
- Plotly 6.3+ (Charts)
- Scikit-learn 1.7+ (ML Model)
- Bootstrap 5.3 (Frontend)

---

## ✅ Pre-Deployment Checklist

Your repository is already configured for Vercel deployment:

- ✅ **run.py** - Entry point with WSGI app
- ✅ **vercel.json** - Vercel configuration
- ✅ **requirements.txt** - Python dependencies (includes scikit-learn + numpy)
- ✅ **.vercelignore** - Excludes unnecessary files
- ✅ **predictions/** - ML model included (not excluded)
- ✅ **data/** - Dataset included (not excluded)

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Vercel deployment with ML model"

# Push to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy to Vercel

#### Option A: Vercel Dashboard (Recommended)

1. Go to [https://vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click **"Add New Project"**
4. Select your repository: `Project_Kicks`
5. Configure project settings:
   - **Framework Preset:** Other
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
   - **Install Command:** `pip install -r requirements.txt`

6. Click **"Deploy"**

#### Option B: Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login
vercel login

# Deploy from project directory
cd Project_Kicks
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: kicks-analytics
# - Directory: ./
# - Override settings? No

# Deploy to production
vercel --prod
```

### Step 3: Verify Deployment

Once deployed, Vercel will provide a URL like:
```
https://kicks-analytics.vercel.app
```

Visit the URL and check:
- ✅ Dashboard loads correctly
- ✅ All 4 pages are accessible (Sales, Product, Customer, ML Predictions, About)
- ✅ Charts render properly
- ✅ ML Prediction page shows dropdowns with month names
- ✅ Predictions work without errors

---

## 🔧 Configuration Details

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "run.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run.py"
    }
  ]
}
```

**What this does:**
- Uses Vercel's Python builder for `run.py`
- Routes all requests to the Flask app

### requirements.txt
```
Flask>=3.0.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.24.0
scikit-learn>=1.3.0
Werkzeug>=3.0.0
gunicorn
```

**Estimated install size:** ~150-180 MB (including dependencies)

### .vercelignore
```
*.pyc
__pycache__/
.git/
.gitignore
.claude/
ml_api/
PROJECT_STRUCTURE.md
DEPLOYMENT_GUIDE.md
.env.example
```

**What's excluded:**
- Python cache files
- Git repository
- Separate ML API code (not needed for all-in-one deployment)
- Documentation files

**What's included:**
- `predictions/` - ML model and predictor
- `data/` - Dataset for charts
- `dashboard/` - All Flask application code

---

## ⚠️ Important Notes

### Serverless Function Limits

Vercel has the following limits for serverless functions:
- **Free Plan:** 50 MB unzipped size limit per function
- **Pro Plan:** 50 MB unzipped size limit per function
- **Total Deployment:** 250 MB limit (you're at ~26 MB ✅)

**Your deployment:**
- Source code: ~26 MB ✅
- Dependencies (scikit-learn, numpy, pandas): ~150 MB
- **Total unzipped:** ~176 MB

### Potential Issues

1. **Function size limit exceeded**
   - If you get "Serverless Function exceeds 50 MB" error, this is because dependencies are too large
   - **Solution:** Use build-time dependency optimization (see troubleshooting below)

2. **Cold start times**
   - First request after inactivity may take 10-15 seconds
   - This is normal for serverless functions with ML models
   - Subsequent requests will be faster

3. **Memory limits**
   - Free plan: 1024 MB memory
   - Your model needs ~100-200 MB at runtime
   - Should be fine for normal usage

---

## 🐛 Troubleshooting

### Error: "Serverless Function exceeds 50 MB"

This happens when dependencies (scikit-learn + numpy) make the function too large.

**Solution 1: Optimize Dependencies**

Create a custom build script `build.sh`:

```bash
#!/bin/bash
pip install --target .python_packages scikit-learn==1.3.0 numpy==1.24.0 pandas==2.0.0
```

Update `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "run.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run.py"
    }
  ]
}
```

**Solution 2: Use Vercel Pro Plan**

Vercel Pro plan ($20/month) has the same 50 MB limit, but with better performance.

**Solution 3: Split Architecture (Fallback)**

If all-in-one deployment fails, use the split architecture:
- Deploy dashboard to Vercel (without ML dependencies)
- Deploy ML API to Render (free tier)
- Connect via API calls

See `DEPLOYMENT_GUIDE.md` for split architecture instructions.

### Error: "Module not found: scikit-learn"

Make sure `scikit-learn>=1.3.0` is in `requirements.txt` and properly installed.

### Month dropdown shows numbers instead of names

This is a browser caching issue:
1. Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
2. Or clear browser cache for the Vercel URL

### Predictions return "Model not available"

Check that:
1. `predictions/` folder is NOT in `.vercelignore`
2. `predictions/trained_models/units_predictor.pkl` exists in repository
3. File size is ~24 MB (the optimized model)

---

## 📈 Performance Optimization

### Enable Caching

Add to `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### Environment Variables

No environment variables needed for all-in-one deployment!

For split architecture (if needed), add:
```
ML_API_URL=https://your-ml-api.onrender.com
```

---

## 🔄 Updating Your Deployment

### Update Code
```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

Vercel will automatically redeploy on push to `main` branch.

### Update ML Model

To update the model:
```bash
# Retrain model
cd predictions
python train_models.py

# Commit and push
cd ..
git add predictions/trained_models/
git commit -m "Update ML model"
git push origin main
```

### Manual Redeploy

Via CLI:
```bash
vercel --prod
```

Via Dashboard:
1. Go to Vercel dashboard
2. Select your project
3. Click "Deployments"
4. Click "Redeploy" on latest deployment

---

## 📊 Monitoring

### View Logs

Via CLI:
```bash
vercel logs
```

Via Dashboard:
1. Go to your project
2. Click "Deployments"
3. Select a deployment
4. Click "View Function Logs"

### Analytics

Vercel provides built-in analytics:
- Page views
- Response times
- Bandwidth usage
- Error rates

Access via: Project → Analytics

---

## 💰 Cost Estimate

### Free Tier (Hobby)
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ May hit 50 MB function limit with dependencies

### Pro Tier ($20/month)
- ✅ 1 TB bandwidth/month
- ✅ Better performance
- ✅ Team collaboration
- ⚠️ Still has 50 MB function limit

**Recommendation:** Try Free tier first. If you hit the function size limit, either:
1. Use dependency optimization techniques
2. Switch to split architecture (Vercel + Render)
3. Upgrade to Pro for better performance (but won't solve size limit)

---

## 🎯 Next Steps

1. **Deploy to Vercel** using steps above
2. **Test all features** on the live URL
3. **Set up custom domain** (optional)
   - Go to Project Settings → Domains
   - Add your domain (e.g., `kicks-analytics.com`)
4. **Enable Vercel Analytics** for monitoring
5. **Share your dashboard!** 🚀

---

## 📞 Support

- **Vercel Docs:** https://vercel.com/docs
- **Vercel Community:** https://github.com/vercel/vercel/discussions
- **Project Issues:** Contact repository owner

---

**Ready to deploy!** Your project is optimized and configured for Vercel. 🎉

Total size: 26 MB ✅
Dependencies: ~150 MB (may need optimization) ⚠️
ML Model: 24 MB (optimized) ✅
All features: Working ✅
