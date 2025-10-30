import streamlit as st
import requests
import tempfile
import os

FLASK_API_URL = "http://127.0.0.1:5000/denoise"

st.set_page_config(page_title="🎧 Audio Denoiser", page_icon="🎵")
st.title("🎶 Audio Denoiser App")
st.write("Upload your noisy audio file and get a clean version!")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "ogg", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    st.info("Processing your audio... Please wait ⏳")

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        # ✅ Send file correctly to Flask
        with open(tmp_path, "rb") as audio:
            files = {"file": (os.path.basename(tmp_path), audio, "audio/wav")}
            response = requests.post(FLASK_API_URL, files=files)

        if response.status_code == 200:
            output_path = "denoised_output.wav"
            with open(output_path, "wb") as f:
                f.write(response.content)

            st.success("✅ Denoising complete!")
            st.audio(output_path, format="audio/wav")
            st.download_button("⬇️ Download Denoised Audio", data=open(output_path, "rb"), file_name="denoised.wav")
        else:
            st.error(f"❌ Error from server: {response.text}")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

    finally:
        os.remove(tmp_path)
