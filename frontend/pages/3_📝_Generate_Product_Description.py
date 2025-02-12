import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("🛍️ AI-Powered Product Description Generator")
if st.button("Generate Description"):
    if "product_title" in st.session_state and st.session_state.product_title and "product_image" in st.session_state and st.session_state.product_image:
        st.spinner("🔍 Analyzing product...")


        # Send request to backend
        response = requests.post(
            "http://localhost:8001/description/generate",
            files={"image": st.session_state.product_image.getvalue()},
            data={"title": st.session_state.product_title}
        )

        if response.status_code == 200:
            description = response.json().get("description", "No description generated.")
            st.success("✅ Product Description Generated:")
            st.write(description)
        else:
            st.error("❌ Failed to generate description. Try again.")
    else:
        st.warning("⚠️ Please upload an image and enter a product title.")
