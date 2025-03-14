import streamlit as st
import subprocess
import os
from PIL import Image

st.image("bridge-Photoroom-2.png", use_container_width=True)

st.title("BrieflyAI 🤖")

description = """
Welcome to BrieflyAI - GenAI Documentation Assistant!

Transform complex consulting reports into clear, actionable insights tailored for your team or clients. 

With our GenAI-powered tool, you can upload detailed project documentation and instantly convert it into the format that best suits your audience—whether it's concise summaries, visual reports, structured process steps, images, or even audio explanations. 

Simply define your role and preferences, and let the GenAI adapt the content for maximum clarity and impact. Perfect for consultants, managers, and stakeholders who need quick, tailored insights without losing critical details!
"""

st.write(description)

st.header("User Profile Settings")

if "position" not in st.session_state:
    st.session_state["position"] = ""
if "modality" not in st.session_state:
    st.session_state["modality"] = "Images"
if "company" not in st.session_state:
    st.session_state["company"] = ""

# User Background Input
position = st.text_input(
    "Enter your background (e.g., Logistics Manager, Transport Coordinator):",
    value=st.session_state["position"]
)

# Industry Field Input
company = st.text_input(
    "Enter your field of industry:",
    value=st.session_state["company"]
)

# Preferred Output Selection
modality = st.radio(
    "Preferred Output Format:",
    ["Images", "Audio"],
    index=0 if st.session_state["modality"] == "Images" else 1
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload Your Consulting Report", type=["pdf"]
)

if st.button("Save Preferences"):
    st.session_state["position"] = position
    st.session_state["modality"] = modality
    st.session_state["company"] = company

    st.success("Preferences saved!")

if uploaded_file and position and company:
    # Save uploaded file to 'pdf/' directory
    pdf_dir = "pdf"
    os.makedirs(pdf_dir, exist_ok=True)
    file_path = os.path.join(pdf_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved as {file_path}")

    # Run Shell Script with User Inputs
    if st.button("Generate Output"):
        command = [
            "bash", "main.sh",
            uploaded_file.name,  # File name
            modality,  # Image or audio
            position,  # User's position
            company  # Company name
        ]

        with st.spinner("Processing... Please wait."):
            result = subprocess.run(command, capture_output=True, text=True)
            st.text_area("Shell Script Output:", result.stdout)

        st.success("Processing Complete!")

        output_folder = uploaded_file.name.replace(".pdf", "")
        
        if modality == "image":
            image_files = [f for f in os.listdir(output_folder) if f.endswith(".jpg")]
            for img in image_files:
                st.image(os.path.join(output_folder, img), caption=img)

        elif modality == "audio":
            audio_files = [f for f in os.listdir(output_folder) if f.endswith(".wav") or f.endswith(".mp3")]
            for audio in audio_files:
                st.audio(os.path.join(output_folder, audio))