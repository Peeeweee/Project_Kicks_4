# Vercel Deployment Guide for Project_Kicks

## Overview
This guide will help you deploy the Adidas Sales Dashboard to Vercel, making it accessible on the web.

## Prerequisites
- A [Vercel account](https://vercel.com/signup) (free tier is sufficient)
- Git installed on your computer
- Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Project Directory**
   ```bash
   cd c:\Users\Paulo\Documents\Project_Kicks
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N` (first time)
   - Project name? `project-kicks` (or your preferred name)
   - In which directory is your code located? `./`
   - Want to override settings? `N`

5. **Production Deployment**
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard (GitHub Integration)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Import Project on Vercel**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your Git repository
   - Vercel will auto-detect the Flask configuration

3. **Configure Project**
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (usually 1-2 minutes)

## Configuration Files

### vercel.json
The `vercel.json` file is already configured for your Flask application:
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

### .vercelignore
Files excluded from deployment:
- `data_cleaning/` - Data processing scripts (not needed in production)
- `instance/` - Flask instance folder
- `*.pyc` - Python compiled files
- `__pycache__/` - Python cache
- `.git/` - Git repository data

**Important:** The CSV data file (`data/adidas_sales_cleaned.csv`) IS included in deployment as it's required for the dashboard to function.

## Environment Variables

Currently, no environment variables are required. The secret key is hardcoded for simplicity.

For production security, consider:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add: `SECRET_KEY` with a random secure value
3. Update `dashboard/__init__.py` to use it:
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
   ```

## Post-Deployment

### Accessing Your Dashboard
After deployment, Vercel will provide you with:
- **Production URL**: `https://your-project-name.vercel.app`
- **Preview URLs**: Auto-generated for each Git push

### Custom Domain (Optional)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### Monitoring
- View logs: Vercel Dashboard → Your Project → Deployments → Click deployment → Logs
- View analytics: Project → Analytics tab

## Troubleshooting

### Common Issues

**Issue: "No Python version specified"**
- Solution: Vercel auto-detects Python 3.9. If issues occur, add to `vercel.json`:
  ```json
  "builds": [{
    "src": "run.py",
    "use": "@vercel/python",
    "config": { "runtime": "python3.9" }
  }]
  ```

**Issue: "Module not found"**
- Solution: Ensure all dependencies are in `requirements.txt`
- Run: `pip freeze > requirements.txt` to update

**Issue: "CSV file not found"**
- Solution: Verify `adidas_sales_cleaned.csv` is NOT in `.vercelignore`
- Check the file exists in `data/` directory before deploying

**Issue: "Application timeout"**
- Vercel serverless functions have a 10-second timeout (free tier)
- For large datasets, consider caching or optimizing data loading

### Deployment Limits (Free Tier)
- 100 GB bandwidth per month
- 100 deployments per day
- 10-second function execution limit
- 1024 MB memory per function

## Local Testing Before Deployment

Always test locally before deploying:
```bash
python run.py
```
Visit: `http://localhost:5001`

## Redeployment

**Automatic:** Push to Git (if connected via GitHub)
```bash
git add .
git commit -m "Update dashboard"
git push
```

**Manual:** Using Vercel CLI
```bash
vercel --prod
```

## Support

- Vercel Documentation: https://vercel.com/docs
- Vercel Python Runtime: https://vercel.com/docs/runtimes#official-runtimes/python
- Project Issues: Check application logs in Vercel dashboard

## Project Structure for Vercel

```
Project_Kicks/
├── run.py                    # WSGI entry point (required)
├── requirements.txt          # Python dependencies (required)
├── vercel.json              # Vercel configuration (required)
├── .vercelignore            # Deployment exclusions
├── dashboard/               # Flask application
│   ├── __init__.py         # App factory
│   ├── data_loader.py      # Data loading
│   ├── api/                # API endpoints
│   ├── pages/              # Page routes
│   ├── static/             # CSS files
│   └── templates/          # HTML templates
└── data/
    └── adidas_sales_cleaned.csv  # Required data file

```

## Next Steps

1. Deploy using one of the methods above
2. Test all dashboard features on the live URL
3. Share your dashboard URL
4. Set up custom domain (optional)
5. Monitor usage and performance

Your Adidas Sales Dashboard is now ready for web deployment!
