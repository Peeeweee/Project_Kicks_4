# 🚀 Quick Deployment Checklist

## Pre-Deployment Verification

- [x] `vercel.json` configured correctly
- [x] `.vercelignore` updated (CSV files are NOT ignored)
- [x] `requirements.txt` includes all dependencies
- [x] `run.py` exposes WSGI `app` variable
- [x] CSV data file exists at `data/adidas_sales_cleaned.csv`
- [ ] Tested locally with `python run.py`
- [ ] All dependencies installed with `pip install -r requirements.txt`

## Deployment Methods

### Method 1: Vercel CLI (Fastest)
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Deploy to production
vercel --prod
```

### Method 2: GitHub + Vercel Dashboard
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Vercel"
git push origin main

# 2. Go to vercel.com/dashboard
# 3. Click "Add New Project"
# 4. Import your repository
# 5. Click "Deploy"
```

## Post-Deployment Checks

- [ ] Dashboard loads successfully
- [ ] All charts render correctly
- [ ] Navigation between tabs works
- [ ] API endpoints respond correctly
- [ ] No console errors in browser

## Your Deployment URLs

**Production URL:** `https://[your-project-name].vercel.app`
**Dashboard:** `https://vercel.com/dashboard`

## Quick Commands

```bash
# Local test
python run.py

# Deploy to Vercel
vercel --prod

# View logs
vercel logs [deployment-url]

# List deployments
vercel ls
```

## Need Help?

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
