import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract
import os
from googletrans import Translator


# ------------------------------
# STREAMLIT CONFIG
# ------------------------------
st.set_page_config(page_title="TEXTEMAGE", layout="wide")

# Load Tesseract path from file (if exists)
if os.path.exists("tesseract_path.txt"):
    with open("tesseract_path.txt", "r") as f:
        pytesseract.pytesseract.tesseract_cmd = f.read().strip()
else:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

translator = Translator()

# Initialize session states
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "extracted_text_area" not in st.session_state:
    st.session_state.extracted_text_area = ""

if "last_image_name" not in st.session_state:
    st.session_state.last_image_name = ""


# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.title("📌 TEXTEMAGE")
st.sidebar.write("### v1.4 (Streamlit Edition)")
st.sidebar.markdown("---")
st.sidebar.write("Developed by **Manjit Chakraborty**")

if st.sidebar.button("📘 About"):
    st.sidebar.info("""
**TEXTEMAGE Streamlit Edition**

- Extract text from images  
- Translate extracted text  
- Uses Tesseract OCR  
- Smooth Streamlit Web UI  
""")


# ------------------------------
# MAIN UI
# ------------------------------
st.title("📸 TEXTEMAGE — Image to Text Extractor + Translator")
st.write("Upload an image, extract text, then translate it easily.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "bmp", "webp"])
col1, col2 = st.columns(2)


# ------------------------------
# IMAGE PREVIEW & EXTRACTION
# ------------------------------
if uploaded_file:

    try:
        img = Image.open(uploaded_file)
    except UnidentifiedImageError:
        st.error("❌ Invalid image file!")
        st.stop()

    with col1:
        st.image(img, caption="Uploaded Image", use_column_width=True)
        st.markdown("### 🔍 Extract Text")

        if st.button("Extract"):
            try:
                text = pytesseract.image_to_string(img)
                st.session_state.extracted_text = text
                st.session_state.extracted_text_area = text
                st.session_state.last_image_name = getattr(uploaded_file, "name", "image")
                st.success("✔ Text extracted successfully!")
            except Exception as e:
                st.error("❌ Tesseract not installed or path is wrong.")
                st.exception(e)
                st.stop()


# ------------------------------
# TEXT BOX (ALWAYS ON RIGHT SIDE)
# ------------------------------
with col2:
    st.markdown("### 📄 Extracted Text")

    # Bind text_area with ONE session key
    extracted = st.text_area(
        "Extracted text (editable)",
        height=250,
        key="extracted_text_area"
    )

    # Keep main extracted_text synced
    st.session_state.extracted_text = extracted

    # Buttons area
    bc1, bc2, bc3 = st.columns([1, 1, 1])

    with bc1:
        if st.button("Clear"):
            st.session_state.extracted_text = ""
            st.session_state.extracted_text_area = ""
            st.experimental_rerun()

    with bc2:
        if st.session_state.extracted_text.strip() != "":
            st.download_button(
                "⬇ Download .txt",
                st.session_state.extracted_text,
                file_name=f"{st.session_state.last_image_name}.txt"
            )

    with bc3:
        if st.session_state.extracted_text.strip() != "":
            st.write("Characters:", len(st.session_state.extracted_text))

    st.markdown("---")


    # ------------------------------
    # TRANSLATION SECTION
    # ------------------------------
    st.markdown("### 🌍 Translate Extracted Text")

    languages = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Assamese": "as",
        "Nepali": "ne",
        "French": "fr",
        "German": "de",
        "Spanish": "es",
        "Japanese": "ja",
        "Korean": "ko",
        "Chinese (Simplified)": "zh-cn"
    }

    if st.session_state.extracted_text.strip() == "":
        st.info("Extract text from an image first to enable translation.")
    else:
        target_lang = st.selectbox("Select language", list(languages.keys()))
        target_code = languages[target_lang]

        if st.button("Translate"):
            try:
                with st.spinner("Translating..."):
                    translated = translator.translate(st.session_state.extracted_text, dest=target_code)
                st.success(f"✔ Translated to {target_lang}")
                st.text_area("Translated text:", translated.text, height=250)
            except Exception as e:
                st.error("Translation failed. Check internet connection or googletrans.")
                st.exception(e)


# ------------------------------
# FOOTER
# ------------------------------
st.markdown("""
---
### ⭐ Made by **Manjit Chakraborty**
""", unsafe_allow_html=True)
