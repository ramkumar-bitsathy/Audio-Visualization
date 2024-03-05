import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def extract_features(audio_path, selected_features):
    y, sr = librosa.load(audio_path)

    features = {}

    if 'MFCC' in selected_features:
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        features['MFCC'] = mfccs

    if 'Chroma' in selected_features:
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features['Chroma'] = chroma

    if 'Spectral Contrast' in selected_features:
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        features['Spectral Contrast'] = contrast

    if 'Tempo' in selected_features:
        onset_env = librosa.onset.onset_strength(y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        features['Tempo'] = tempo

    return features

def plot_tempo(tempo):
    col2.text(f"Estimated Tempo: {tempo} BPM")

def plot_features(features):
    for feature_name, feature_data in features.items():
        col2.subheader(feature_name)

        if feature_name == 'Tempo':
            plot_tempo(feature_data)
        else:
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(feature_data, x_axis='time')
            plt.colorbar()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            col2.pyplot()
            
def main():
    #st.set_page_config(page_title="Audio Feature Visualizer", page_icon="🎵")
    st.title("Audio Feature Visualizer")
    
    # Left Column: Uploading and Feature Selection
    global col2
    col1, col2 = st.columns(2,gap="large")

    uploaded_file = col1.file_uploader("Choose an audio file", type=["mp3", "wav"])

    if uploaded_file is not None:
        col1.subheader("Feature Selection")
        show_mfcc = col1.checkbox("MFCC", True)
        show_chroma = col1.checkbox("Chroma", True)
        show_spectral_contrast = col1.checkbox("Spectral Contrast", True)
        show_tempo = col1.checkbox("Tempo", True)

        selected_features = []

        if show_mfcc:
            selected_features.append('MFCC')
        if show_chroma:
            selected_features.append('Chroma')
        if show_spectral_contrast:
            selected_features.append('Spectral Contrast')
        if show_tempo:
            selected_features.append('Tempo')

        # Right Column: Image Visualization
        col2.subheader("Selected Features Visualization")

        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            col2.audio(audio_bytes, format="audio")

            features = extract_features(BytesIO(audio_bytes), selected_features)
            plot_features(features)

if __name__ == "__main__":
    main()
