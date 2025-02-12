import streamlit as st
from io import BytesIO
from PIL import Image

# Initialize session state for storing product data
if "product_title" not in st.session_state:
    st.session_state.product_title = ""
if "product_image" not in st.session_state:
    st.session_state.product_image = None


# Homepage Content
st.title("Welcome to AI Product Assistant! 🚀")
st.subheader("Enter product details and let AI do the magic!")

# Input for product title
product_title = st.text_input("Enter Product Title", st.session_state.product_title)

# Image uploader
uploaded_image = st.file_uploader("Upload a Product Image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Store in session state
    # img_bytes = BytesIO()
    # image.save(img_bytes, format="PNG")
    st.session_state.product_image = uploaded_image
    st.session_state.product_title = product_title

# "Let the Magic Begin" Button
if st.button("✨ Let the Magic Begin ✨"):
    if product_title and uploaded_image:
        st.success("Product saved! Navigate using the sidebar.")
    else:
        st.error("⚠️ Please enter a product title and upload an image.")
