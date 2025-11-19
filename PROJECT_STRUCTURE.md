# Project Structure - Kicks Analytics Dashboard

**Total Project Size:** 51 MB (optimized from ~130 MB)

## 📁 Directory Structure

```
Project_Kicks/
├── .git/                          # Git repository
├── .claude/                       # Claude Code configuration
├── dashboard/                     # Main Flask application
│   ├── __init__.py               # App factory
│   ├── data_loader.py            # CSV data loading
│   ├── pages/                    # Blueprint modules
│   │   ├── sales/                # Sales overview page
│   │   ├── product/              # Product analysis page
│   │   ├── customer/             # Customer insights page
│   │   ├── ml_prediction/        # ML prediction page (calls external API)
│   │   └── about/                # About page
│   ├── templates/                # HTML templates (Jinja2)
│   ├── static/                   # CSS, JS, images
│   └── api/                      # Chart data API endpoints
├── data/                          # Dataset
│   └── adidas_sales_cleaned.csv  # 1.3 MB - 9,648 sales records
├── predictions/                   # ML module (for local dev)
│   ├── predictor.py              # Model loading & prediction
│   ├── train_models.py           # Model training script
│   └── trained_models/           # Trained ML models
│       ├── units_predictor.pkl   # 24 MB - Optimized Random Forest
│       └── metadata.json         # Dropdown values & model info
├── ml_api/                        # Standalone ML API (deploy to Render)
│   ├── app.py                    # Flask API for ML predictions
│   ├── requirements.txt          # API dependencies
│   ├── Procfile                  # Render deployment config
│   ├── runtime.txt               # Python version
│   ├── README.md                 # Deployment instructions
│   └── test_api.py               # API testing script
├── run.py                         # Main entry point (local dev)
├── requirements.txt               # Dashboard dependencies (Vercel)
├── vercel.json                    # Vercel deployment config
├── .vercelignore                  # Files to exclude from Vercel
├── .env.example                   # Environment variables template
└── DEPLOYMENT_GUIDE.md            # Complete deployment guide
```

---

## 🎯 Core Files (Production)

### Essential for Deployment:

**Dashboard (Vercel):**
- `dashboard/` - All dashboard code
- `data/adidas_sales_cleaned.csv` - Dataset for charts
- `run.py` - Entry point
- `requirements.txt` - Python dependencies
- `vercel.json` - Deployment configuration
- `.vercelignore` - Exclude ML files

**ML API (Render):**
- `ml_api/` - Entire folder
- `predictions/predictor.py` - Model loader
- `predictions/train_models.py` - Training script
- `predictions/trained_models/` - Model files (24 MB optimized)

---

## 📊 Key Features

### Dashboard (20+ Interactive Charts):
1. Sales Overview - Time series, trends, totals
2. Product Analysis - Category performance, price analysis
3. Customer Insights - Regional analysis, retailer performance
4. ML Predictions - AI-powered demand forecasting

### ML Model:
- **Algorithm:** Random Forest Regressor
- **Performance:** 82.89% Revenue R², 75.80% Units R²
- **Size:** 24.09 MB (optimized from 63 MB)
- **Features:** 60 trees, max_depth=18, dynamic confidence intervals

---

## 🗑️ Deleted Files (Cleanup)

### Root Directory:
- ❌ `analyze_model.py` - Model analysis script
- ❌ `create_snapshot.py` - Snapshot utility
- ❌ `project_snapshot.txt` - 1.4 MB snapshot file
- ❌ `setup_ml_predictions.py` - Setup script
- ❌ `test_app.py` - Test file
- ❌ `package-lock.json` - Empty npm file

### Predictions:
- ❌ `optimize_model_size.py` - Optimization script (already used)
- ❌ `apply_optimization.py` - Application script (already used)
- ❌ `units_predictor_old_63mb.pkl` - Old 63 MB model
- ❌ `sales_predictor.pkl` - Unused model

### Folders:
- ❌ `data_cleaning/` - Development scripts
- ❌ `instance/` - Flask runtime folder
- ❌ `demand_predictor/` - Old experimental code

**Total Space Saved:** ~79 MB

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────┐
│     Vercel (Frontend/Dashboard)     │
│  - Flask app                        │
│  - 20+ interactive charts           │
│  - Data visualizations              │
│  - Size: ~27 MB (under 250 MB)      │
└──────────────┬──────────────────────┘
               │
               │ HTTP API Calls
               │ (ML_API_URL env var)
               │
               ▼
┌─────────────────────────────────────┐
│       Render (ML API Backend)       │
│  - Random Forest model (24 MB)      │
│  - Prediction engine                │
│  - Confidence intervals             │
│  - Size: ~50 MB                     │
└─────────────────────────────────────┘
```

---

## 📦 Dependencies

### Dashboard (requirements.txt):
- Flask 3.0.0 - Web framework
- pandas 2.0.0 - Data processing
- plotly 5.18.0 - Interactive charts
- Werkzeug 3.0.0 - WSGI utilities
- requests 2.31.0 - HTTP library
- gunicorn - WSGI server

### ML API (ml_api/requirements.txt):
- Flask 3.0.0
- flask-cors 4.0.0 - CORS support
- pandas 2.0.0
- numpy 1.24.0
- scikit-learn 1.3.0 - ML framework
- gunicorn 21.2.0

---

## 🔧 Configuration Files

### `.vercelignore`
Excludes from Vercel deployment:
- `predictions/` - ML module (handled by Render)
- `ml_api/` - Separate API code
- Development files

### `vercel.json`
```json
{
  "version": 2,
  "builds": [{"src": "run.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "run.py"}]
}
```

### Environment Variables (Vercel):
- `ML_API_URL` - URL of Render ML API
  - Example: `https://kicks-ml-api.onrender.com`

---

## 📈 Performance Metrics

### Model Performance:
- Revenue R²: **82.89%**
- Units R²: **75.80%**
- Revenue MAE: **$3,160**
- Units MAE: **68.1 units**

### Model Size Optimization:
- Original: 63.0 MB
- Optimized: 24.09 MB
- **Reduction: 61.8%**
- **Savings: 38.91 MB**

### Dataset:
- Records: 9,648 sales transactions
- Size: 1.3 MB
- Features: 18 columns
- Time Period: 2020-2021

---

## 🎓 Technologies Used

**Backend:**
- Python 3.11+
- Flask 3.1.2
- Pandas 2.3.3
- NumPy 2.2.6
- Plotly 6.3.1
- Scikit-learn 1.7.2

**Frontend:**
- Bootstrap 5.3.0
- Plotly.js
- Font Awesome 6.4.0
- Google Fonts (Montserrat)

**ML:**
- Random Forest Regressor
- Label Encoding
- 95% Confidence Intervals
- Dynamic Scoring

**Deployment:**
- Vercel (Dashboard)
- Render (ML API)
- Git/GitHub
- Gunicorn WSGI

---

## 📝 Next Steps

1. ✅ Model optimized (61.8% smaller)
2. ✅ Unnecessary files cleaned up
3. ⏳ Ready to commit and deploy

**Commit command:**
```bash
git add .
git commit -m "Optimize ML model and clean up project - 61.8% size reduction"
git push origin main
```

**Then deploy:**
- Render: Redeploy ML API with 24 MB model
- Vercel: Should already be deployed

---

**Total Production Size:** 51 MB (Dashboard + ML + Data)
- Vercel deployment: ~27 MB
- Render deployment: ~50 MB (includes model)
- Both well under platform limits! ✅
