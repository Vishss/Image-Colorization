# 🎨 Colorful Image Colorization App

This is a **Streamlit-based application** for automatic **colorization of black & white images** with additional **image editing tools** and **multi-format download options**.
It integrates deep learning models (`eccv16` and `siggraph17`) for realistic colorization and provides professional editing features like brightness, contrast, saturation, hue shift, and filters.

---

## 🚀 Features

* **Upload & Colorize**

  * Upload black & white images (`.jpg`, `.jpeg`, `.png`)
  * Choose between **ECCV16** and **SIGGRAPH17** models for colorization

* **Output Resolution Options**

  * Original size
  * Preset sizes: **256×256**, **512×512**, **1024×1024**
  * Custom size (64–4096 px width/height)

* **Real-Time Editing Tools**

  * **Brightness** adjustment
  * **Contrast** adjustment
  * **Saturation** adjustment
  * **Hue Shift** (-180° to +180°)
  * **Filters**: Vintage, Cool Tone, Warm Tone, Dramatic

* **Download Options**

  * Export in multiple formats: **PNG, JPG, PDF, TIFF**

* **UI Highlights**

  * Side-by-side comparison: **original vs edited**
  * Reset button for quick revert
  * Sidebar with editing guide

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/colorization_app.git
cd colorization_app
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

* Windows:

```bash
venv\Scripts\activate
```

* macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Typical requirements:

```
streamlit
torch
numpy
pillow
```

### 4. Run the app

```bash
streamlit run colorization_editor_app.py
```

---

## 📖 How to Use

1. Upload a **black & white image**.
2. Select the **model** (`eccv16` or `siggraph17`).
3. Choose the **output resolution** (original, preset, or custom).
4. Click **"Colorize Image"**.
5. Adjust with **sliders & filters** (brightness, contrast, saturation, hue shift, effects).
6. Compare **original vs edited** results side by side.
7. Download the final output in your desired **format (PNG, JPG, PDF, TIFF)**.

---

