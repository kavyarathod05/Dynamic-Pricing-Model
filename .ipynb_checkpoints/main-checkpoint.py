from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load your models
preprocessor = joblib.load("preprocessor.pkl")
demand_model = joblib.load("demand_forecast_model.pkl")
discount_model = joblib.load("discount_prediction_model.pkl")

# FastAPI app
app = FastAPI()

# Input schema
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

@app.post("/predict/")
def predict(item: Item):
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
    return {"demand_forecast": demand, "discount_prediction": discount}
