# streamlit_app.py
import streamlit as st
from audio_recorder import record_audio
import librosa
import matplotlib.pyplot as plt
import numpy as np

def plot_pitch_variation(audio_path, pitch_threshold_low=160, pitch_threshold_high=1450):
    # Load audio file
    rec = r"C:\Users\RAMKUMAR K\Desktop\Audio Visualisation\recorded_audio.wav"
    y1, sr1 = librosa.load(audio_path)
    y2,sr2 = librosa.load(rec)

    # Apply pre-emphasis to enhance high-frequency content (optional but can be beneficial)
    y1_preemphasized = librosa.effects.preemphasis(y1)
    y2_preemphasized = librosa.effects.preemphasis(y2)

    # Extract pitch using the yin algorithm
    pitch1, magnitudes, *_ = librosa.core.pyin(y=y1_preemphasized, fmin=50, fmax=2000, sr=sr1)
    pitch1 = np.where(pitch1 < pitch_threshold_low, np.nan, pitch1)
    first_non_nan_index1 = np.argmax(~np.isnan(pitch1))
    pitch1 = pitch1[first_non_nan_index1:]

    pitch1 = pitch1 - (pitch1[0]-130.81)

    rec_pitch ,magnitudes2,*_ = librosa.core.pyin(y=y2_preemphasized,fmin=50,fmax=2000,sr=sr2)
    rec_pitch = np.where(rec_pitch < pitch_threshold_low, np.nan, rec_pitch)
    first_non_nan_index2 = np.argmax(~np.isnan(rec_pitch))
    rec_pitch = rec_pitch[first_non_nan_index2:]
    # Convert frame indices to time
    rec_pitch = rec_pitch - (rec_pitch[0]-130.81)
    times = librosa.times_like(pitch1)
    rec_times = librosa.times_like(rec_pitch)

    # Customize plot
    plt.title('Pitch Variation Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Pitch (Hz)')
    plt.grid(True)


    # Plot the pitch variation
    plt.plot(times, pitch1, label='Pitch (Hz)',color='y')
    plt.plot(rec_times,rec_pitch,color='r')

    return plt

def main():
    st.title("Learning App")
    col1,col2 = st.columns(2,gap="large")


    uploaded_file = col1.file_uploader("Choose an audio file", type=["wav"])
    col1.audio(uploaded_file, format='audio/wav')

    # Audio recorder settings
    col2.subheader("Learner! record your Audio")
    recording_button = col2.button("Start Recording")
    recording_duration = col2.slider("Select recording duration (seconds)", min_value=1, max_value=20, value=10)

    if recording_button:
        col2.write("Recording...")
        record_audio("recorded_audio.wav", duration=recording_duration)
        col2.write(f"Recording complete! Duration: {recording_duration} seconds")
    col2.audio("recorded_audio.wav", format='audio/wav')


    if uploaded_file is not None:
        

        # Set pitch threshold values
        col2.subheader("Select Pitch Threshold")
        pitch_threshold_low = col2.slider("Select lower pitch threshold", min_value=50, max_value=500, value=160)
        pitch_threshold_high = col2.slider("Select upper pitch threshold", min_value=100, max_value=2000, value=1450)
        if st.button("Plot"):
            # Plot pitch variation
            plt = plot_pitch_variation(uploaded_file, pitch_threshold_low, pitch_threshold_high)
            # Display plot in Streamlit
            st.pyplot(plt)
        

if __name__ == "__main__":
    main()