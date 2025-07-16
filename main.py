from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML models
try:
    preprocessor = joblib.load("preprocessor.pkl")
    demand_model = joblib.load("demand_forecast_model.pkl")
    discount_model = joblib.load("discount_prediction_model.pkl")
except Exception as e:
    print(f"Model loading error: {e}")
    raise

# Request input schema
class Item(BaseModel):
    Store_ID: str
    Product_ID: str
    Inventory_Level: float
    Units_Sold: float
    Units_Ordered: float
    Price: float
    Competitor_Pricing: float
    Weather_Condition: str
    Seasonality: str

# Root route (for health check)
@app.get("/")
def root():
    return {"message": "✅ Dynamic Pricing API is live!"}

# Prediction endpoint
@app.post("/predict/")
def predict(item: Item):
    try:
        df = pd.DataFrame([{
            'Store ID': item.Store_ID,
            'Product ID': item.Product_ID,
            'Inventory Level': item.Inventory_Level,
            'Units Sold': item.Units_Sold,
            'Units Ordered': item.Units_Ordered,
            'Price': item.Price,
            'Competitor Pricing': item.Competitor_Pricing,
            'Weather Condition': item.Weather_Condition,
            'Seasonality': item.Seasonality
        }])

        transformed = preprocessor.transform(df)
        demand = demand_model.predict(transformed)[0]
        discount = discount_model.predict(transformed)[0]

        print(f"✅ Prediction successful: Demand={demand}, Discount={discount}")
        return {
            "demand_forecast": round(float(demand), 2),
            "discount_prediction": round(float(discount), 2)
        }

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return {"error": str(e)}
