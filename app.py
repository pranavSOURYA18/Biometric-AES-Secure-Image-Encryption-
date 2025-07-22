import streamlit as st
from PIL import Image
import numpy as np
import sys
import os
import io

# Add utils path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth import login_user, signup_user
from utils.biometric_key import generate_key_from_face
from utils.encryption import encrypt_image, decrypt_image
from utils.visualizer import visualize_cipher
from utils.steganography import lsb_embed, lsb_extract

# ------------------ LOGIN SYSTEM ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Secure Image Encryption Portal")
    st.markdown("Welcome to **Biometric AES Encryption with Steganography**.\nPlease log in or sign up to continue.")
    action = st.radio("Select Action", ["Login", "Signup"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(action):
        if action == "Login":
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
        else:
            ok, msg = signup_user(username, password)
            if ok:
                st.success(msg + " You can now login.")
            else:
                st.error(msg)
    st.stop()

# ------------------ MAIN APP START ------------------
st.set_page_config(page_title="Biometric AES Encryption", layout="wide")
st.title("🔐 Biometric-AES Image Encryption with Steganography")
st.sidebar.markdown(f"👤 Logged in as: `{st.session_state.username}`")
st.sidebar.markdown("**AES Mode:** CBC (Fixed)")
mode = "CBC"

face_img = st.sidebar.file_uploader("Upload Face Image (for Key)", type=["jpg", "jpeg", "png"])
key = None
if face_img:
    face_image_pil = Image.open(face_img).convert("RGB")
    face_image_np = np.array(face_image_pil)
    try:
        key = generate_key_from_face(face_image_np)
        st.sidebar.success("✅ Biometric Key Generated")
    except Exception as e:
        st.sidebar.error(f"Face Recognition Error: {e}")

tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# ------------------------ ENCRYPTION ------------------------
with tab1:
    st.markdown("### Step 1: Upload Image to Encrypt")
    img_file = st.file_uploader("Choose an image to encrypt", type=["jpg", "png", "bmp"])

    if img_file and key is not None:
        img = Image.open(img_file).convert("RGB")
        img_np = np.array(img)
        original_shape = img_np.shape

        ciphertext, iv = encrypt_image(img_np, key, mode)

        st.image(img, caption="Original Image", use_column_width=True)
        st.markdown("### Step 2: Visualize Ciphertext")
        try:
            enc_img = visualize_cipher(ciphertext, original_shape)
            st.image(enc_img, caption="Cipher Visualization")
        except Exception as viz_err:
            st.warning(f"Visualization skipped: {viz_err}")

        st.markdown("### Step 3: Embed into Cover Image")
        cover_file = st.file_uploader("Upload Cover Image (same or larger)", type=["jpg", "png"])
        if cover_file:
            cover_np = np.array(Image.open(cover_file).convert("RGB"))
            try:
                shape_bytes = np.array(original_shape, dtype=np.uint16).tobytes()
                hidden_data = iv + shape_bytes + ciphertext
                stego = lsb_embed(cover_np, hidden_data)
                st.image(stego, caption="Stego Image", use_column_width=True)
                output = io.BytesIO()
                Image.fromarray(stego).save(output, format="PNG")
                st.download_button("Download Stego Image", output.getvalue(), file_name="stego_output.png")
            except Exception as e:
                st.error(f"Embedding failed: {e}")

# ------------------------ DECRYPTION ------------------------
with tab2:
    st.markdown("### Step 1: Upload Stego Image to Decrypt")
    stego_upload = st.file_uploader("Upload previously embedded image", type=["png"])
    if stego_upload and key is not None:
        try:
            stego_img = np.array(Image.open(stego_upload).convert("RGB"))
            hidden_data = lsb_extract(stego_img)
            iv = hidden_data[:16]
            shape_bytes = hidden_data[16:22]
            shape = tuple(np.frombuffer(shape_bytes, dtype=np.uint16))
            ciphertext = hidden_data[22:]

            decrypted = decrypt_image(ciphertext, iv, key, mode)
            decrypted_img = np.frombuffer(decrypted, dtype=np.uint8).reshape(shape)
            st.image(decrypted_img, caption="Decrypted Image", use_column_width=True)
        except Exception as e:
            st.error(f"Decryption failed: {e}")
