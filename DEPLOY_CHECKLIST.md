# 🚀 Vercel Deployment Checklist

Quick checklist to deploy Kicks Analytics Dashboard to Vercel.

---

## Pre-Deployment ✅

- [x] Model optimized to 24 MB
- [x] Month dropdown uses names (January, February, etc.)
- [x] All dependencies in requirements.txt
- [x] vercel.json configured
- [x] .vercelignore configured
- [x] predictions/ folder included (NOT excluded)
- [x] data/ folder included (NOT excluded)
- [x] Total size: 26 MB (under 250 MB limit)

---

## Deployment Steps 📋

### 1. Test Locally
```bash
python run.py
```
- [ ] Visit http://localhost:5001
- [ ] Check all 5 pages load
- [ ] Test ML predictions with month names
- [ ] Verify charts render correctly

### 2. Commit Changes
```bash
git add .
git commit -m "Ready for Vercel deployment"
```

### 3. Push to GitHub
```bash
git push origin main
```

### 4. Deploy to Vercel

**Option A: Vercel Dashboard**
- [ ] Go to https://vercel.com
- [ ] Sign in with GitHub
- [ ] Click "Add New Project"
- [ ] Select repository
- [ ] Click "Deploy"

**Option B: Vercel CLI**
```bash
npm install -g vercel
vercel login
vercel --prod
```

### 5. Verify Deployment
- [ ] Visit deployed URL
- [ ] Test Sales Overview page
- [ ] Test Product Analysis page
- [ ] Test Customer Patterns page
- [ ] Test ML Predictions page
  - [ ] Dropdown shows month names
  - [ ] Make a test prediction
  - [ ] Check results display correctly
- [ ] Test About page

---

## Post-Deployment 🎉

### Optional Enhancements
- [ ] Add custom domain
- [ ] Enable Vercel Analytics
- [ ] Set up monitoring
- [ ] Configure caching headers

### Share Your Work
- [ ] Copy deployment URL
- [ ] Share with stakeholders
- [ ] Add to portfolio
- [ ] Update README with live link

---

## If Deployment Fails ⚠️

**Error: "Serverless Function exceeds 50 MB"**
- Dependencies (scikit-learn + numpy) are too large
- See VERCEL_DEPLOYMENT.md for solutions
- Consider split architecture (Vercel + Render)

**Other Issues**
- Check deployment logs in Vercel dashboard
- See troubleshooting section in VERCEL_DEPLOYMENT.md
- Ensure all required files are committed

---

## Quick Commands

```bash
# Local testing
python run.py

# Commit changes
git add .
git commit -m "Your message"
git push origin main

# Deploy via CLI
vercel --prod

# View logs
vercel logs

# Check deployment status
vercel ls
```

---

**Ready to deploy? Follow the steps above! 🚀**

For detailed instructions, see: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
