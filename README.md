# 👟 Kicks Analytics Dashboard

**Adidas US Sales Analytics Platform with AI-Powered Demand Forecasting**

A comprehensive Flask-based analytics dashboard featuring 20+ interactive visualizations and machine learning predictions for Adidas sales data.

![Dashboard Status](https://img.shields.io/badge/status-ready%20to%20deploy-success)
![Model Size](https://img.shields.io/badge/model-24.09%20MB-blue)
![Model Accuracy](https://img.shields.io/badge/revenue%20R²-82.89%25-green)

---

## 🎯 Features

### 📊 Interactive Analytics
- **Sales Overview** - Time series analysis, revenue trends, key metrics
- **Product Analysis** - Category performance, price optimization insights
- **Customer Patterns** - Regional analysis, retailer performance breakdowns
- **About** - Project overview, tech stack, model performance metrics

### 🤖 AI-Powered Predictions
- **Demand Forecasting** - Predict units sold and revenue
- **Dynamic Confidence Intervals** - 95% prediction uncertainty ranges
- **Real-time Insights** - Instant predictions with confidence scoring
- **Model Performance Tracking** - Live R² and MAE metrics

---

## 📈 Dashboard Highlights

### 20+ Interactive Charts
- Revenue trends over time
- Sales by region and retailer
- Product category breakdowns
- Price distribution analysis
- Monthly and quarterly patterns
- Top performing products
- And more...

### ML Prediction Engine
- **Algorithm:** Optimized Random Forest Regressor
- **Model Size:** 24.09 MB (61.8% reduction from 63 MB)
- **Revenue R²:** 82.89% (excellent prediction accuracy)
- **Units R²:** 75.80% (strong demand forecasting)
- **Revenue MAE:** $3,160 (average prediction error)
- **Units MAE:** 68 units (average prediction error)

---

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Project_Kicks.git
cd Project_Kicks

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Open browser
# http://localhost:5001
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

Or deploy via [Vercel Dashboard](https://vercel.com) by connecting your GitHub repository.

**For detailed deployment instructions, see:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

---

## 📁 Project Structure

```
Project_Kicks/
├── dashboard/                  # Flask application
│   ├── __init__.py            # App factory
│   ├── data_loader.py         # CSV data loading
│   ├── pages/                 # Blueprint modules
│   │   ├── sales/             # Sales overview
│   │   ├── product/           # Product analysis
│   │   ├── customer/          # Customer insights
│   │   ├── ml_prediction/     # ML predictions
│   │   └── about/             # About page
│   ├── templates/             # Jinja2 templates
│   ├── static/                # CSS, JS, images
│   └── api/                   # Chart data endpoints
├── data/                       # Dataset
│   └── adidas_sales_cleaned.csv  # 9,648 sales records (1.3 MB)
├── predictions/                # ML module
│   ├── predictor.py           # Prediction service
│   ├── train_models.py        # Model training
│   └── trained_models/        # Trained models
│       ├── units_predictor.pkl   # 24 MB Random Forest
│       └── metadata.json      # Model configuration
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── vercel.json                # Vercel configuration
├── .vercelignore              # Deployment exclusions
└── README.md                  # This file
```

**Total Size:** 26 MB (optimized for deployment)

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.0+** - Web framework
- **Pandas 2.0+** - Data processing
- **NumPy 1.24+** - Numerical computing
- **Scikit-learn 1.3+** - Machine learning
- **Gunicorn** - WSGI server

### Frontend
- **Bootstrap 5.3** - UI framework
- **Plotly 6.3+** - Interactive charts
- **Font Awesome 6.4** - Icons
- **Google Fonts** - Typography (Montserrat)

### ML Model
- **Random Forest Regressor** - Optimized hyperparameters
  - n_estimators: 60 trees
  - max_depth: 18
  - min_samples_split: 3
- **Label Encoding** - Categorical feature transformation
- **Confidence Intervals** - 95% prediction uncertainty

### Deployment
- **Vercel** - Serverless hosting
- **GitHub** - Version control
- **Python 3.11+** - Runtime

---

## 📊 Dataset

**Adidas US Sales Data (2020-2021)**
- **Records:** 9,648 sales transactions
- **Size:** 1.3 MB
- **Features:** 18 columns
  - Retailer, Region, Product, Sales Method
  - Price per Unit, Units Sold, Total Sales
  - Operating Profit, Operating Margin
  - Invoice Date, Month, Quarter

**Source:** Cleaned and processed from original Adidas sales dataset

---

## 🤖 ML Model Details

### Training Process
```bash
cd predictions
python train_models.py
```

### Model Performance
| Metric | Units Sold | Revenue |
|--------|-----------|---------|
| **R² Score** | 75.80% | 82.89% |
| **MAE** | 68.1 units | $3,160 |
| **RMSE** | 106.88 units | $5,309 |

### Optimization Journey
- **Original Model:** 63 MB (100 trees)
- **Optimized Model:** 24.09 MB (60 trees)
- **Size Reduction:** 61.8% smaller
- **Accuracy Impact:** +0.07% improvement in Revenue R²

### Prediction Features
The model predicts based on:
- Retailer (Amazon, Foot Locker, Walmart, etc.)
- Region (Northeast, South, West, etc.)
- Product category (Footwear, Apparel)
- Sales method (In-store, Online, Outlet)
- Price per unit ($7-$110)
- Month (January-December)
- Quarter (Q1-Q4)

---

## 📖 Documentation

- **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)** - Complete deployment guide
- **[DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)** - Quick deployment checklist
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Detailed project structure
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Split architecture guide (Vercel + Render)

---

## 🎨 Screenshots

### Sales Overview
Interactive time series charts showing revenue trends, total sales, and key performance metrics.

### ML Predictions
AI-powered demand forecasting with:
- Dropdown inputs (Retailer, Region, Product, etc.)
- Month selection (January-December)
- Real-time predictions with confidence intervals
- Model performance metrics

### Analytics Pages
- Product category performance analysis
- Regional sales breakdowns
- Retailer comparison charts
- Price distribution insights

---

## 🔄 Updates & Maintenance

### Retrain ML Model
```bash
cd predictions
python train_models.py
git add predictions/trained_models/
git commit -m "Update ML model"
git push origin main
```

### Update Dashboard
```bash
# Make changes to dashboard code
git add .
git commit -m "Update dashboard features"
git push origin main
```

Vercel will automatically redeploy on push to `main` branch.

---

## 🐛 Troubleshooting

### Month Dropdown Shows Numbers
**Issue:** Dropdown displays "1, 2, 3..." instead of "January, February, March..."

**Solution:**
1. Hard refresh browser: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
2. Clear browser cache for localhost:5001

### Model Not Loading
**Issue:** "Model not available" error on ML Predictions page

**Solution:**
1. Check `predictions/trained_models/units_predictor.pkl` exists
2. Verify file size is ~24 MB
3. Ensure `predictions/` is not in `.vercelignore`
4. Restart Flask app: `python run.py`

### Vercel Deployment Fails
**Issue:** "Serverless Function exceeds 50 MB" error

**Solution:** See troubleshooting section in [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

---

## 📝 License

This project is created for educational and portfolio purposes.

Dataset: Adidas US Sales Data (publicly available)

---

## 👤 Author

**Project:** Kicks Analytics Dashboard
**Tech Stack:** Flask, Scikit-learn, Plotly, Bootstrap
**Deployment:** Vercel (All-in-One)

---

## 🙏 Acknowledgments

- Adidas sales dataset
- Flask framework
- Scikit-learn library
- Plotly visualization library
- Bootstrap UI framework
- Vercel hosting platform

---

## 📞 Support

For issues or questions:
- Check [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for deployment help
- Review [troubleshooting section](#-troubleshooting) above
- Open an issue on GitHub

---

**Built with ❤️ using Flask, Machine Learning, and Modern Web Technologies**

🚀 **Ready to deploy!** See [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md) to get started.
