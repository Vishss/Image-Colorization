import streamlit as st
from PIL import Image
import numpy as np
import torch
from colorizers import eccv16, siggraph17, preprocess_img, postprocess_tens, load_img

st.title("Colorful Image Colorization")

uploaded_file = st.file_uploader("Upload a black & white image", type=["jpg", "jpeg", "png"])
model_option = st.selectbox("Choose model", ["eccv16", "siggraph17"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    img.save("temp_input.png")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Load model
    if model_option == "eccv16":
        colorizer = eccv16(pretrained=True).eval()
    else:
        colorizer = siggraph17(pretrained=True).eval()

    # Preprocess and colorize
    img_np = np.array(img)
    tens_l_orig, tens_l_rs = preprocess_img(img_np, HW=(256,256))
    out_img = postprocess_tens(tens_l_orig, colorizer(tens_l_rs).cpu())

    st.image(out_img, caption="Colorized Image", use_column_width=True)
    st.download_button("Download Colorized Image", data=Image.fromarray((out_img*255).astype(np.uint8)).tobytes(), file_name="colorized.png", mime="image/png")