# Project_Kicks - Vercel Deployment

## 🎯 Overview
This Adidas Sales Dashboard is fully configured for deployment on Vercel's serverless platform.

## ⚡ Quick Start - Deploy Now!

### Option A: One-Command Deployment
```bash
npx vercel --prod
```

### Option B: GitHub Auto-Deploy
1. Push to GitHub: `git push origin main`
2. Import on [vercel.com](https://vercel.com/new)
3. Click Deploy - Done! ✅

## 📋 What's Configured

### ✅ Vercel Configuration Files
- **[vercel.json](vercel.json)** - Serverless function configuration
- **[.vercelignore](.vercelignore)** - Deployment exclusions
- **[run.py](run.py)** - WSGI application entry point
- **[requirements.txt](requirements.txt)** - Python dependencies

### ✅ Included in Deployment
- Flask application (`dashboard/`)
- Static files (CSS)
- Templates (HTML)
- **CSV data file** (`data/adidas_sales_cleaned.csv`) - 1.3MB
- All Python dependencies

### ❌ Excluded from Deployment
- Data cleaning scripts
- Git files
- Python cache files
- Development utilities

## 🏗️ Architecture on Vercel

```
Vercel Edge Network
        ↓
   Serverless Function (run.py)
        ↓
   Flask Application
        ↓
   ┌─────────┬─────────┬──────────┐
   │   API   │  Pages  │  Static  │
   └─────────┴─────────┴──────────┘
        ↓
   CSV Data (1.3MB)
```

## 📊 Deployment Specifications

| Specification | Value |
|--------------|-------|
| Platform | Vercel Serverless |
| Runtime | Python 3.9 |
| Function Timeout | 10s (Free), 60s (Pro) |
| Memory | 1024 MB |
| Data Size | ~1.3 MB (CSV) |
| Cold Start | ~1-2 seconds |
| Concurrent Users | 1000+ (Pro) |

## 🚀 Deployment Steps

### First Time Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   Answer prompts:
   - Project name: `project-kicks` (or your choice)
   - Directory: `./`
   - Settings: Accept defaults

4. **Production Deploy**
   ```bash
   vercel --prod
   ```

### Subsequent Deployments

```bash
# Preview deployment
vercel

# Production deployment
vercel --prod
```

## 🔧 Configuration Details

### vercel.json Explained
```json
{
  "version": 2,
  "builds": [{
    "src": "run.py",           // Entry point
    "use": "@vercel/python"    // Python runtime
  }],
  "routes": [{
    "src": "/(.*)",            // All routes
    "dest": "run.py"           // Go to Flask app
  }]
}
```

### Key Features
- **Serverless Functions**: Each request handled by isolated function
- **Auto-scaling**: Handles traffic spikes automatically
- **Global CDN**: Serves static files from edge locations
- **Zero Configuration**: Works out of the box

## 🌐 URLs After Deployment

You'll receive:
- **Production URL**: `https://project-kicks.vercel.app`
- **Preview URLs**: Generated for each deployment
- **Custom Domain**: Can be added in settings

## 📈 Performance Optimization

### Already Optimized:
✅ CSV data loaded once per function instance (cached)
✅ Pandas DataFrames reused across requests
✅ Static files served from CDN
✅ Gzip compression enabled automatically

### Vercel Benefits:
- **Smart Caching**: Functions stay warm for repeat requests
- **Edge Network**: Content served from nearest location
- **Automatic HTTPS**: SSL certificates included
- **DDoS Protection**: Built-in security

## 🔐 Security Recommendations

### For Production:
1. Set environment variable for secret key:
   ```bash
   vercel env add SECRET_KEY production
   ```

2. Update `dashboard/__init__.py`:
   ```python
   import os
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback')
   ```

## 🐛 Troubleshooting

### Issue: Deployment Fails
**Check:**
- Requirements.txt has all dependencies
- CSV file exists in data/
- No syntax errors: `python -m py_compile run.py`

### Issue: CSV Not Found
**Solution:**
- Verify `data/adidas_sales_cleaned.csv` exists
- Check it's NOT in `.vercelignore`
- Redeploy with `vercel --prod`

### Issue: Timeout Errors
**Causes:**
- Large data processing (>10s on free tier)
- Upgrade to Pro for 60s timeout
- Or optimize data loading

### View Logs
```bash
vercel logs [deployment-url]
```

## 💰 Pricing

### Free Tier (Hobby)
- ✅ Perfect for this project
- 100 GB bandwidth/month
- 100 deployments/day
- 10s function timeout
- Free SSL & CDN

### Pro Tier ($20/month)
- 1 TB bandwidth
- 60s function timeout
- Better analytics
- Team collaboration

## 📚 Resources

- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Checklist**: [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)
- **Vercel Docs**: https://vercel.com/docs
- **Python on Vercel**: https://vercel.com/docs/runtimes#official-runtimes/python

## 🎯 Quick Commands Reference

```bash
# Deploy to production
vercel --prod

# View deployments
vercel ls

# View logs
vercel logs

# Remove deployment
vercel rm [deployment-name]

# Local development
python run.py
```

## ✅ Pre-Deployment Checklist

Before deploying, ensure:
- [ ] Local test works: `python run.py` → http://localhost:5001
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] CSV file exists: `ls data/adidas_sales_cleaned.csv`
- [ ] Git committed: `git status` (if using GitHub)

## 🎉 Ready to Deploy!

Your Project_Kicks dashboard is **fully configured** and ready for Vercel deployment.

### Deploy Now:
```bash
vercel --prod
```

Your dashboard will be live in ~60 seconds! 🚀

---

**Questions?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
