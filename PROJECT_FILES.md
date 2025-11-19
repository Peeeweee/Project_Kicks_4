# Final Project Structure for Vercel Deployment

## ✅ Files to Deploy (Vercel)

```
Project_Kicks/
├── dashboard/              # Flask application
│   ├── __init__.py
│   ├── data_loader.py
│   ├── api/               # Chart data endpoints
│   ├── pages/             # All page blueprints
│   │   ├── sales/
│   │   ├── product/
│   │   ├── customer/
│   │   ├── ml_prediction/
│   │   └── about/
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, images
├── data/                  # Dataset
│   └── adidas_sales_cleaned.csv
├── run.py                 # Entry point
├── requirements-vercel.txt # Lightweight dependencies
├── vercel.json            # Vercel config
├── .vercelignore          # Exclusions
└── README.md              # Documentation
```

## ❌ Excluded from Vercel (in .vercelignore)

- `ml_api/` - Separate ML API (deploy to Render)
- `predictions/` - ML model (too large for Vercel)
- `requirements.txt` - Full dependencies (not used)
- `SPLIT_DEPLOYMENT.md` - Documentation

## 📦 Total Vercel Deployment Size

- Dashboard code: ~500 KB
- Data (CSV): 1.3 MB
- Dependencies (pandas, plotly, flask): ~25-30 MB
- **Total: ~30 MB** ✅ (under 250 MB limit)

## 🚀 Ready to Deploy

```bash
git add .
git commit -m "Clean up for Vercel deployment"
git push origin main
```

Then deploy on Vercel dashboard!
