import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract
import os
from deep_translator import GoogleTranslator

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(page_title="TEXTEMAGE", layout="wide")

# Set Tesseract Path
if os.path.exists("tesseract_path.txt"):
    with open("tesseract_path.txt", "r") as f:
        pytesseract.pytesseract.tesseract_cmd = f.read().strip()
else:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ------------------------------
# SESSION STATE
# ------------------------------
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "last_image_name" not in st.session_state:
    st.session_state.last_image_name = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

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
- Fully deployable on Streamlit Cloud
""")

# ------------------------------
# MAIN APP
# ------------------------------
st.title("📸 TEXTEMAGE — Image to Text Extractor + Translator")
st.write("Upload an image, extract text, and translate it.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "bmp", "webp"])
col1, col2 = st.columns(2)

# ------------------------------
# IMAGE UPLOAD & OCR
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

        # OCR Extraction button
        if st.button("Extract Text from Image"):
            try:
                st.session_state.extracted_text = pytesseract.image_to_string(img)
                st.session_state.last_image_name = getattr(uploaded_file, "name", "uploaded_image")
                st.session_state.translated_text = ""  # reset translated text
                st.success("✔ Text Extracted Successfully!")
            except Exception as e:
                st.error("❌ Tesseract not installed or not found in PATH.")
                st.exception(e)

# ------------------------------
# EXTRACTED TEXT DISPLAY
# ------------------------------
with col2:
    st.markdown("### 📄 Extracted Text")

    # Bind text_area directly to session_state.extracted_text
    st.session_state.extracted_text = st.text_area(
        "Extracted text (you can edit before translating):",
        value=st.session_state.extracted_text,
        height=250
    )

    # Utilities
    util_col1, util_col2, util_col3 = st.columns([1,1,1])
    with util_col1:
        if st.button("Clear Text"):
            st.session_state.extracted_text = ""
            st.session_state.translated_text = ""
            st.experimental_rerun()
    with util_col2:
        if st.session_state.extracted_text.strip() != "":
            st.download_button(
                "⬇ Download .txt",
                st.session_state.extracted_text,
                file_name=f"{st.session_state.last_image_name or 'extracted'}.txt",
                mime="text/plain"
            )
    with util_col3:
        if st.session_state.extracted_text.strip() != "":
            st.write("Characters:", len(st.session_state.extracted_text))

st.markdown("---")

# ------------------------------
# TRANSLATION
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
    "Chinese (Simplified)": "zh-cn",
}

if st.session_state.extracted_text.strip() == "":
    st.info("No extracted text to translate — first extract text from an image.")
    st.selectbox("Choose language", list(languages.keys()), index=0, disabled=True)
    st.button("Translate", disabled=True)
else:
    selected = st.selectbox("Choose language", list(languages.keys()), index=0)
    if st.button("Translate Text"):
        target_code = languages[selected]
        text_to_translate = st.session_state.extracted_text
        try:
            with st.spinner("Translating..."):
                st.session_state.translated_text = GoogleTranslator(
                    source='auto', target=target_code
                ).translate(text_to_translate)
            st.success(f"✔ Translated to {selected}!")
        
        except Exception as e:
            st.error("❌ Translation failed. Check your internet connection.")
            st.exception(e)

    # Show translated text
    if st.session_state.translated_text.strip() != "":
        st.text_area(f"Translated text ({selected}):", value=st.session_state.translated_text, height=250)

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("""
---
### ⭐ Made by **Manjit Chakraborty**
""", unsafe_allow_html=True)
