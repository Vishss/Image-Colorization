import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import torch
from colorizers import eccv16, siggraph17, preprocess_img, postprocess_tens, load_img
import io
import os

st.title("Colorful Image Colorization")

uploaded_file = st.file_uploader("Upload a black & white image", type=["jpg", "jpeg", "png"])
model_option = st.selectbox("Choose model", ["eccv16", "siggraph17"])

# Resolution options
st.sidebar.header("Output Settings")
resolution_options = {
    "Original": "original",
    "256x256": (256, 256),
    "512x512": (512, 512),
    "1024x1024": (1024, 1024),
    "Custom": "custom"
}

resolution_choice = st.sidebar.selectbox("Output Resolution", list(resolution_options.keys()))

custom_width = 512
custom_height = 512

if resolution_choice == "Custom":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        custom_width = st.number_input("Width", min_value=64, max_value=4096, value=512)
    with col2:
        custom_height = st.number_input("Height", min_value=64, max_value=4096, value=512)

# Download format options
download_formats = st.sidebar.multiselect(
    "Download Formats",
    ["PNG", "JPG", "PDF", "SVG", "TIFF"],
    default=["PNG"]
)

# Initialize session state for edited image
if 'colorized_img' not in st.session_state:
    st.session_state.colorized_img = None
if 'edited_img' not in st.session_state:
    st.session_state.edited_img = None
if 'adjustments' not in st.session_state:
    st.session_state.adjustments = {
        'brightness': 1.0,
        'contrast': 1.0,
        'saturation': 1.0,
        'hue_shift': 0.0,
        'filter': 'none'
    }
if 'original_size' not in st.session_state:
    st.session_state.original_size = None
if 'current_output_size' not in st.session_state:
    st.session_state.current_output_size = None

def get_output_size(original_size):
    """Get the current output size based on user selection"""
    if resolution_choice == "Original":
        return original_size
    elif resolution_choice == "Custom":
        return (custom_width, custom_height)
    else:
        return resolution_options[resolution_choice]

def resize_image_to_output(image, original_size):
    """Resize image to the current output size"""
    output_size = get_output_size(original_size)
    if output_size != original_size:
        return image.resize(output_size, Image.Resampling.LANCZOS)
    return image

def apply_adjustments(image, adjustments):
    """Apply all adjustments to the image"""
    img = image.copy()
    
    # Brightness
    if adjustments['brightness'] != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(adjustments['brightness'])
    
    # Contrast
    if adjustments['contrast'] != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(adjustments['contrast'])
    
    # Saturation
    if adjustments['saturation'] != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(adjustments['saturation'])
    
    # Hue Shift (convert to HSV, modify, convert back)
    if adjustments['hue_shift'] != 0.0:
        img = img.convert('HSV')
        h, s, v = img.split()
        
        # Shift hue (0-360 degrees, but PIL uses 0-255 for hue)
        hue_shift = int(adjustments['hue_shift'] * 255 / 360)
        h = h.point(lambda x: (x + hue_shift) % 255)
        
        img = Image.merge('HSV', (h, s, v)).convert('RGB')
    
    # Apply filters
    if adjustments['filter'] == 'vintage':
        # Vintage effect: slight sepia tone
        img = apply_vintage_filter(img)
    elif adjustments['filter'] == 'cool':
        # Cool tone: boost blues
        img = apply_cool_filter(img)
    elif adjustments['filter'] == 'warm':
        # Warm tone: boost reds/yellows
        img = apply_warm_filter(img)
    elif adjustments['filter'] == 'dramatic':
        # Dramatic: high contrast and saturation
        img = apply_dramatic_filter(img)
    
    return img

def apply_vintage_filter(img):
    """Apply vintage/sepia filter"""
    # Convert to sepia-like tones
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    img_array = np.array(img).astype(np.float32) / 255.0
    sepia_array = np.dot(img_array, sepia_filter.T)
    sepia_array = np.clip(sepia_array, 0, 1) * 255
    
    vintage_img = Image.fromarray(sepia_array.astype(np.uint8))
    
    # Add slight blur for vintage look
    vintage_img = vintage_img.filter(ImageFilter.GaussianBlur(0.7))
    
    return vintage_img

def apply_cool_filter(img):
    """Apply cool tone filter (boost blues)"""
    img_array = np.array(img).astype(np.float32)
    
    # Boost blue channel, reduce red
    img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.2, 0, 255)  # Blue
    img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 0.9, 0, 255)  # Red
    
    return Image.fromarray(img_array.astype(np.uint8))

def apply_warm_filter(img):
    """Apply warm tone filter (boost reds/yellows)"""
    img_array = np.array(img).astype(np.float32)
    
    # Boost red and green channels
    img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.2, 0, 255)  # Red
    img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.1, 0, 255)  # Green
    
    return Image.fromarray(img_array.astype(np.uint8))

def apply_dramatic_filter(img):
    """Apply dramatic high-contrast filter"""
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    dramatic_img = enhancer.enhance(1.5)
    
    # Increase saturation
    enhancer = ImageEnhance.Color(dramatic_img)
    dramatic_img = enhancer.enhance(1.3)
    
    # Increase brightness slightly
    enhancer = ImageEnhance.Brightness(dramatic_img)
    dramatic_img = enhancer.enhance(1.1)
    
    return dramatic_img

# Callback functions for real-time updates
def update_brightness():
    st.session_state.adjustments['brightness'] = st.session_state.brightness_slider

def update_contrast():
    st.session_state.adjustments['contrast'] = st.session_state.contrast_slider

def update_saturation():
    st.session_state.adjustments['saturation'] = st.session_state.saturation_slider

def update_hue_shift():
    st.session_state.adjustments['hue_shift'] = st.session_state.hue_shift_slider

def update_filter():
    filter_options = {
        "None": "none",
        "Vintage": "vintage", 
        "Cool Tone": "cool",
        "Warm Tone": "warm",
        "Dramatic": "dramatic"
    }
    st.session_state.adjustments['filter'] = filter_options[st.session_state.filter_select]

def get_current_filter_key():
    """Safely get the current filter key with error handling"""
    filter_options = {
        "None": "none",
        "Vintage": "vintage", 
        "Cool Tone": "cool",
        "Warm Tone": "warm",
        "Dramatic": "dramatic"
    }
    
    current_filter = st.session_state.adjustments['filter']
    
    # Find the key for the current filter value
    matching_keys = [k for k, v in filter_options.items() if v == current_filter]
    
    if matching_keys:
        return matching_keys[0]
    else:
        # If no match found, default to "None"
        st.session_state.adjustments['filter'] = 'none'
        return "None"

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    original_size = img.size
    st.session_state.original_size = original_size
    
    # Get current output size
    current_output_size = get_output_size(original_size)
    st.session_state.current_output_size = current_output_size
    
    st.image(img, caption=f"Uploaded Image ({original_size[0]}x{original_size[1]})", use_container_width=True)

    # Colorize button
    if st.button("Colorize Image") or st.session_state.colorized_img is not None:
        if st.session_state.colorized_img is None:
            # Load model
            if model_option == "eccv16":
                colorizer = eccv16(pretrained=True).eval()
            else:
                colorizer = siggraph17(pretrained=True).eval()

            # Preprocess and colorize
            with st.spinner("Colorizing image..."):
                img_np = np.array(img)
                tens_l_orig, tens_l_rs = preprocess_img(img_np, HW=(256,256))
                out_img = postprocess_tens(tens_l_orig, colorizer(tens_l_rs).cpu())
                
                # Convert to PIL Image
                colorized_pil = Image.fromarray((out_img * 255).astype(np.uint8))
                
                # Store original colorized image
                st.session_state.colorized_img = colorized_pil
                st.session_state.edited_img = colorized_pil.copy()
        
        # Display current resolution info
        st.info(f"🖼️ Current Output Resolution: {current_output_size[0]}x{current_output_size[1]}")
        
        # Apply adjustments to the base colorized image first
        base_edited_img = apply_adjustments(st.session_state.colorized_img, st.session_state.adjustments)
        
        # Then resize to current output size for display
        display_edited_img = resize_image_to_output(base_edited_img, st.session_state.original_size)
        st.session_state.edited_img = display_edited_img
        
        # Display colorized images side by side
        st.subheader("Colorized Image Comparison")
        
        # Create two columns for side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            display_colorized_img = resize_image_to_output(st.session_state.colorized_img, st.session_state.original_size)
            st.image(display_colorized_img, caption=f"Original Colorized ({current_output_size[0]}x{current_output_size[1]})", use_container_width=True)
        
        with col2:
            st.image(display_edited_img, caption=f"Edited Version ({current_output_size[0]}x{current_output_size[1]})", use_container_width=True)
        
        # Image Editing Controls
        st.subheader("🎨 Real-Time Image Editing")
        st.write("Adjust the sliders below to edit your colorized image. Changes apply instantly!")
        
        # Basic Adjustments
        st.markdown("### Basic Adjustments")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.slider(
                "Brightness", 
                min_value=0.0, 
                max_value=2.0, 
                value=st.session_state.adjustments['brightness'],
                step=0.1,
                key="brightness_slider",
                on_change=update_brightness
            )
        
        with col2:
            st.slider(
                "Contrast", 
                min_value=0.0, 
                max_value=2.0, 
                value=st.session_state.adjustments['contrast'],
                step=0.1,
                key="contrast_slider",
                on_change=update_contrast
            )
        
        with col3:
            st.slider(
                "Saturation", 
                min_value=0.0, 
                max_value=2.0, 
                value=st.session_state.adjustments['saturation'],
                step=0.1,
                key="saturation_slider",
                on_change=update_saturation
            )
        
        with col4:
            st.slider(
                "Hue Shift", 
                min_value=-180.0, 
                max_value=180.0, 
                value=st.session_state.adjustments['hue_shift'],
                step=5.0,
                key="hue_shift_slider",
                on_change=update_hue_shift
            )
        
        # Filters/Effects
        st.markdown("### 🎭 Filters & Effects")
        
        filter_options = {
            "None": "none",
            "Vintage": "vintage", 
            "Cool Tone": "cool",
            "Warm Tone": "warm",
            "Dramatic": "dramatic"
        }
        
        # Safely get current filter key
        current_filter_key = get_current_filter_key()
        
        st.selectbox(
            "Choose Filter",
            list(filter_options.keys()),
            index=list(filter_options.keys()).index(current_filter_key),
            key="filter_select",
            on_change=update_filter
        )
        
        # Reset button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Reset All Adjustments", use_container_width=True):
                st.session_state.adjustments = {
                    'brightness': 1.0,
                    'contrast': 1.0,
                    'saturation': 1.0,
                    'hue_shift': 0.0,
                    'filter': 'none'
                }
                st.rerun()

        # Download section for edited image
        st.header("📥 Download Edited Image")
        st.write(f"Downloading at: **{current_output_size[0]}x{current_output_size[1]}** resolution")
        
        # Create download buttons in columns for better layout
        cols = st.columns(len(download_formats))
        
        for i, fmt in enumerate(download_formats):
            with cols[i]:
                # Apply adjustments and resize for download
                base_edited = apply_adjustments(st.session_state.colorized_img, st.session_state.adjustments)
                download_img = resize_image_to_output(base_edited, st.session_state.original_size)
                
                if fmt == "PNG":
                    img_buffer = io.BytesIO()
                    download_img.save(img_buffer, format='PNG', quality=100)
                    st.download_button(
                        label="Download PNG",
                        data=img_buffer.getvalue(),
                        file_name=f"colorized_{current_output_size[0]}x{current_output_size[1]}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                elif fmt == "JPG":
                    img_buffer = io.BytesIO()
                    rgb_img = download_img.convert('RGB')
                    rgb_img.save(img_buffer, format='JPEG', quality=95)
                    st.download_button(
                        label="Download JPG",
                        data=img_buffer.getvalue(),
                        file_name=f"colorized_{current_output_size[0]}x{current_output_size[1]}.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                
                elif fmt == "PDF":
                    img_buffer = io.BytesIO()
                    rgb_img = download_img.convert('RGB')
                    rgb_img.save(img_buffer, format='PDF')
                    st.download_button(
                        label="Download PDF",
                        data=img_buffer.getvalue(),
                        file_name=f"colorized_{current_output_size[0]}x{current_output_size[1]}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                elif fmt == "TIFF":
                    img_buffer = io.BytesIO()
                    download_img.save(img_buffer, format='TIFF', compression='tiff_lzw')
                    st.download_button(
                        label="Download TIFF",
                        data=img_buffer.getvalue(),
                        file_name=f"colorized_{current_output_size[0]}x{current_output_size[1]}.tiff",
                        mime="image/tiff",
                        use_container_width=True
                    )

# Add some information in the sidebar
st.sidebar.header("About")
st.sidebar.info(
    """
    **Features:**
    - Multiple colorization models
    - Customizable output resolution
    - Real-time image editing
    - Multiple download formats
    - Professional filters and effects
    """
)

st.sidebar.header("Editing Guide")
st.sidebar.text(
    """
    Brightness: Overall lightness
    Contrast: Light/dark difference  
    Saturation: Color intensity
    Hue Shift: Color tone change
    Filters: Instant effects
    """
)