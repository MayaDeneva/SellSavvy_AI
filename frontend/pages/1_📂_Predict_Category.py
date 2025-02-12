import streamlit as st
import requests

st.title("📂 Predict Product Category")

if "product_title" in st.session_state and st.session_state.product_title:
    st.subheader(f"🔍 Predicting Category for: {st.session_state.product_title}")

    def predict_category(title):
        """Call FastAPI backend to predict category"""
        response = requests.post(
            "http://localhost:8001/categorization/predict",
            json={"title": title}
        )
        if response.status_code == 200:
            return response.json().get("category", "Unknown")
        return "Unknown"

    if st.button("🔮 Predict Category"):
        category = predict_category(st.session_state.product_title)
        st.session_state.generated_category = category
        st.success(f"✅ Predicted Category: **{category}**")

else:
    st.warning("⚠️ Please enter a product title and upload an image on the Home page first.")
