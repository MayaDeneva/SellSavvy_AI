import streamlit as st
import requests
import io
from PIL import Image

st.title("Remove Background from Product Image")

if "product_image" in st.session_state and st.session_state.product_image:
    if st.button("Remove Background"):
        with st.spinner("🔍 Processing with AI..."):
            files = {"image": st.session_state.product_image.getvalue()}  # Send as file
            response = requests.post("http://localhost:8001/background/remove_background", files=files)

            if response.status_code == 200:
                #  Read processed image directly from response
                processed_image = Image.open(io.BytesIO(response.content))

                #  Display processed image
                st.image(processed_image, caption="Background Removed (AI)", use_container_width=True)

                #  Allow user to download
                st.download_button("Download Image", data=response.content, file_name="background_removed.png", mime="image/png")

            else:
                st.error("❌ Failed to remove background. Try again.")