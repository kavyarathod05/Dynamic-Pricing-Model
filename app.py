import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="Dynamic Pricing Predictor", page_icon="📊", layout="centered")

# Sidebar branding/info
st.sidebar.title("🛍️ Dynamic Pricing Tool")
st.sidebar.markdown("""
This tool predicts:
- **📦 Product demand**
- **💸 Suggested discount**

Powered by your ML backend (FastAPI).
""")
st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Kavya & Naman")

# Main heading
st.title("📈 Dynamic Pricing Predictor")
st.markdown("Predict **demand** and **discount** based on store, product, pricing, and seasonal conditions.")

# Input form
with st.form("predict_form"):
    col1, col2 = st.columns(2)

    with col1:
        Store_ID = st.text_input("🏬 Store ID")
        Product_ID = st.text_input("🛒 Product ID")
        Inventory_Level = st.number_input("📦 Inventory Level", min_value=0.0, value=100.0)
        Units_Sold = st.number_input("✅ Units Sold", min_value=0.0, value=50.0)
        Units_Ordered = st.number_input("📥 Units Ordered", min_value=0.0, value=75.0)

    with col2:
        Price = st.number_input("💰 Current Price", min_value=0.0, value=10.0)
        Competitor_Pricing = st.number_input("📉 Competitor Price", min_value=0.0, value=9.5)
        Weather_Condition = st.selectbox("🌤️ Weather", ["Sunny", "Rainy", "Cloudy", "Snowy"])
        Seasonality = st.selectbox("🗓️ Seasonality", ["High", "Medium", "Low"])

    submit = st.form_submit_button("🔍 Predict")

# Handle submission
if submit:
    data = {
        "Store_ID": Store_ID,
        "Product_ID": Product_ID,
        "Inventory_Level": Inventory_Level,
        "Units_Sold": Units_Sold,
        "Units_Ordered": Units_Ordered,
        "Price": Price,
        "Competitor_Pricing": Competitor_Pricing,
        "Weather_Condition": Weather_Condition,
        "Seasonality": Seasonality
    }

    with st.spinner("Making predictions... 🚀"):
        try:
            response = requests.post("https://dynamic-pricing-model-copv.onrender.com/predict/", json=data)

            if response.status_code == 200:
                result = response.json()

                if "error" in result:
                    st.error(f"❌ Server error: {result['error']}")
                else:
                    st.success("✅ Prediction Successful!")
                    col1, col2 = st.columns(2)
                    col1.metric("📦 Forecasted Demand", result['demand_forecast'])
                    col2.metric("💸 Suggested Discount", f"{result['discount_prediction']}%")
            else:
                st.error(f"❌ Request failed. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Could not reach backend: {e}")
