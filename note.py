import streamlit as st
import os
import onset_detection as on
import Note_extractor as ex

# Function to process uploaded audio and extract notes
def process_audio_and_extract_notes(audio_file):
    # Set a variable to store the uploaded audio path
    uploaded_audio_path = None
    notes = []

    if audio_file is not None:
        # Get the file name
        file_name = audio_file.name

        # Save the uploaded audio file to a temporary location
        temp_audio_path = os.path.join("temp", file_name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_audio_path, "wb") as temp_file:
            temp_file.write(audio_file.read())

        # Store the path to the uploaded audio file
        uploaded_audio_path = temp_audio_path

        # Perform the processing here
        on.save_segments(uploaded_audio_path)
        notes = ex.extract_notes(r'C:\Users\RAMKUMAR K\Desktop\Audio Visualisation\Segmented')

    return uploaded_audio_path, notes

# Main Streamlit code
def main():
    st.title("Musical Notes Extraction🎶🎵🎹")

    # Create a file upload widget
    audio_file = st.file_uploader("Upload an audio file", type=["wav"])
    is_processing = False

    if audio_file is not None:
        # Show a loading spinner
        with st.spinner("Processing..."):
            # Process audio and extract notes
            uploaded_audio_path, notes = process_audio_and_extract_notes(audio_file)
            is_processing = True

        # Display the uploaded audio path
        if uploaded_audio_path is not None:
            st.audio(uploaded_audio_path, format="audio/mpeg")

        # Display the extracted notes
        if is_processing:
            st.header("Extracted Notes:")
            st.write(f"{notes}")
