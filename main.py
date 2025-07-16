# 1. ALL IMPORTS GO AT THE TOP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

# 2. INITIALIZE THE FASTAPI APP
app = FastAPI()

# 3. ADD THE CORS MIDDLEWARE (IMMEDIATELY AFTER INITIALIZING THE APP)
# This is the most critical step.
origins = [
    "null",
    "http://localhost",
     "http://localhost:8001",  # <-- ADD THIS LINE
    "http://127.0.0.1",
    "http://127.0.0.1:5500", # Add any other local ports you use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

# 4. LOAD YOUR MODELS
try:
    preprocessor = joblib.load("preprocessor.pkl")
    demand_model = joblib.load("demand_forecast_model.pkl")
    discount_model = joblib.load("discount_prediction_model.pkl")
except Exception as e:
    print(f"Error loading models: {e}")
    # In a real app, you might want to handle this more gracefully
    raise

# 5. DEFINE YOUR PYDANTIC INPUT SCHEMA
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

# 6. DEFINE YOUR API ROUTES (LAST)
# Added HEAD to fix Render's health check log error
@app.get("/", methods=["GET", "HEAD"])
def root():
    return {"message": "✅ Dynamic Pricing API is live!"}


@app.post("/predict/")
def predict(item: Item):
    try:
        # Your prediction logic
        df = pd.DataFrame([item.dict()])
        
        # This renaming logic assumes your model was trained with spaces in column names
        df.rename(columns={
            'Store_ID': 'Store ID',
            'Product_ID': 'Product ID',
            'Inventory_Level': 'Inventory Level',
            'Units_Sold': 'Units Sold',
            'Units_Ordered': 'Units Ordered',
            'Competitor_Pricing': 'Competitor Pricing',
            'Weather_Condition': 'Weather Condition'
        }, inplace=True)

        transformed = preprocessor.transform(df)
        demand = demand_model.predict(transformed)[0]
        discount = discount_model.predict(transformed)[0]

        return {
            "demand_forecast": round(float(demand), 2),
            "discount_prediction": round(float(discount), 2)
        }

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return {"error": str(e)}