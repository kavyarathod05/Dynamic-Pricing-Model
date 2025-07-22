# 🧠 Dynamic Pricing & Demand Forecasting System

This project builds a complete **ML-powered system** that:
- Predicts **product demand**
- Suggests **optimal discount**
based on inventory, sales, price, competitor pricing, seasonality, and weather.

It includes:
- Data preprocessing
- Model training with stacking ensembles
- Interactive predictions via **Streamlit**
- REST API via **FastAPI**

---

## 📁 Dataset

The dataset used is `retail_store_inventory.csv` with columns like:

- `Store ID`
- `Product ID`
- `Inventory Level`
- `Units Sold`
- `Units Ordered`
- `Price`
- `Competitor Pricing`
- `Weather Condition`
- `Seasonality`
- `Discount`
- `Demand Forecast`

---

## 🔧 Tech Stack

| Layer        | Library/Tool         |
|--------------|----------------------|
| Language     | Python               |
| Data         | Pandas, NumPy        |
| ML Models    | LightGBM, XGBoost, RandomForest, GradientBoosting (via Stacking) |
| API Backend  | FastAPI              |
| Frontend UI  | Streamlit            |
| Deployment   | Uvicorn (local), joblib (model storage) |

---

## 📊 Pipeline Overview

### 1. **Preprocessing**
- Removed unnecessary columns (`Category`, `Region`, `Holiday/Promotion`)
- Handled missing values
- Encoded categorical features with `OneHotEncoder`
- Scaled numerical features with `StandardScaler`
- Combined using `ColumnTransformer`

### 2. **Model Training**
- Two separate targets:
  - `Demand Forecast`
  - `Discount`
- Used **StackingRegressor** with base learners:
  - LightGBM, XGBoost, RandomForest, Gradient Boosting
- Meta-model: **Linear Regression**
- Trained on 80/20 split
- Saved using `joblib`

### 3. **Model Evaluation**
Each model prints:
- MAE
- RMSE
- R² Score
- MAPE-based Accuracy

### 4. **Serving Predictions**
- Saved models:  
  - `demand_forecast_model.pkl`  
  - `discount_prediction_model.pkl`  
  - `preprocessor.pkl`
- Predicts demand and discount using either backend (API) or frontend (UI)

---

## 🧪 Sample Input Format

```json
{
  "Store_ID": "S001",
  "Product_ID": "P0001",
  "Inventory_Level": 231.0,
  "Units_Sold": 127.0,
  "Units_Ordered": 55.0,
  "Price": 33.50,
  "Competitor_Pricing": 29.69,
  "Weather_Condition": "Rainy",
  "Seasonality": "Autumn"
}
