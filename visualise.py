import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

with open("visualise.css","r") as readFile:
    css = readFile.read()
st.markdown(f"<style>{css}</style>",unsafe_allow_html=True)



class plot:
    def __init__(self,audio_path):
        self.audio_path = audio_path
        self.y ,self.sr = librosa.load(self.audio_path)
        self.y_harmonic ,self.y_percussive = librosa.effects.hpss(self.y)
        st.subheader("Audio's waveform")
        plt.figure(figsize=(15,5))
        plt.plot(self.y)
        st.pyplot()

    def plot_mfcc(self):
        st.subheader('MFCCs')
        self.mfccs = librosa.feature.mfcc(y=self.y_harmonic,sr=self.sr)
        plt.figure(figsize=(15, 5))
        librosa.display.specshow(self.mfccs, x_axis='time')
        plt.colorbar()
        st.pyplot()

    def plot_chroma(self):
        st.subheader("Chroma")
        self.chroma=librosa.feature.chroma_cens(y=self.y_harmonic, sr=self.sr)
        plt.figure(figsize=(15, 5))
        librosa.display.specshow(self.chroma,y_axis='chroma', x_axis='time')
        plt.colorbar()
        st.pyplot()

    def plot_harmonicAndPercusive(self):
        st.subheader('Harmonic + Percussive')
        plt.figure(figsize=(15, 5))
        librosa.display.waveshow(self.y_harmonic, sr=self.sr, alpha=0.25)
        librosa.display.waveshow(self.y_percussive, sr=self.sr, color='r', alpha=0.5)
        st.pyplot()

    def plot_tempo(self):
        tempo, beat_frames = librosa.beat.beat_track(y=self.y_harmonic, sr=self.sr)
        st.subheader('Tempo\n '+str(int(tempo))+ ' beats/min (approx.)')
        beat_times = librosa.frames_to_time(beat_frames, sr=self.sr)
        beat_time_diff=np.ediff1d(beat_times)
        beat_nums = np.arange(1, np.size(beat_times))
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 5)
        ax.set_ylabel("Time difference (s)")
        ax.set_xlabel("Beats")
        plt.bar(beat_nums, beat_time_diff)
        st.pyplot()

    def plot_spectralCentroid(self):
        st.subheader('Spectral Centroid')
        cent = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        plt.figure(figsize=(15,5))
        plt.subplot(1, 1, 1)
        plt.semilogy(cent.T, label='Spectral centroid')
        plt.ylabel('Hz')
        plt.xticks([])
        plt.xlim([0, cent.shape[-1]])
        plt.legend()
        st.pyplot()

    def plot_spectralContrast(self):
        st.subheader('Spectral Contrast')
        self.contrast=librosa.feature.spectral_contrast(y=self.y_harmonic,sr=self.sr)
        plt.figure(figsize=(15,5))
        librosa.display.specshow(self.contrast, x_axis='time')
        plt.colorbar()
        plt.ylabel('Frequency bands')
        plt.title('Spectral contrast')
        st.pyplot()

    def plot_spectralRolloff(self):
        st.subheader('Spectral Roll-off')
        self.rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)
        plt.figure(figsize=(15,5))
        plt.semilogy(self.rolloff.T, label='Roll-off frequency')
        plt.ylabel('Hz')
        plt.xticks([])
        plt.xlim([0, self.rolloff.shape[-1]])
        plt.legend()
        st.pyplot()

    def plot_zeroCrossingRate(self):
        st.subheader("Zero Crossing Rate")
        self.zrate=librosa.feature.zero_crossing_rate(self.y_harmonic)
        plt.figure(figsize=(15,5))
        plt.semilogy(self.zrate.T, label='Fraction')
        plt.ylabel('Fraction per Frame')
        plt.xticks([])
        plt.xlim([0, self.rolloff.shape[-1]])
        plt.legend()
        st.pyplot()
    

def extract_and_plot_features(audio_path,selected_features):
    plotter = plot(audio_path)
    
    if 'MFCC' in selected_features:
        plotter.plot_mfcc()
    if 'CHROMA' in selected_features:
        plotter.plot_chroma()
    if 'BEAT' in selected_features:
        plotter.plot_tempo()
    if 'HPLUSP' in selected_features:
        plotter.plot_harmonicAndPercusive()
    if 'CENT' in selected_features:
        plotter.plot_spectralCentroid()
    if 'CONT' in selected_features:
        plotter.plot_spectralContrast()
    if 'ROLLOFF' in selected_features:
        plotter.plot_spectralRolloff()
    if 'ZCR' in selected_features:
        plotter.plot_zeroCrossingRate()
        
def main():
    st.title("Audio Visualization")
    
    uploaded_file = st.file_uploader("Upload wav",type=["wav"])
    st.subheader("Select fetures to be plotted")
    col1 , col2 = st.columns(2)
    
    show_mfcc = col1.checkbox("MFCC",True)
    show_beat = col1.checkbox("Beats",True)
    show_chroma = col1.checkbox("Chroma",True)
    show_harmo_percu = col1.checkbox("Harmonic + Percusive",True)
    show_spectral_centroid = col2.checkbox("Spectral centroid",True)
    show_spectral_contrast = col2.checkbox("Spectral contrast",True)
    show_spectral_rolloff = col2.checkbox("Spectral Roll-off",True)
    show_zero_crossing_rate = col2.checkbox('Zero Crossing Rate',True)
    plot = st.button("Plot")
    
    if uploaded_file and plot:
        
        with st.spinner("Plotting features..."):
            selected_features = []

            if show_mfcc:
                selected_features.append('MFCC')
            if show_beat:
                selected_features.append('BEAT')
            if show_chroma:
                selected_features.append('CHROMA')
            if show_harmo_percu:
                selected_features.append("HPLUSP")
            if show_spectral_centroid:
                selected_features.append('CENT')
            if show_spectral_contrast:
                selected_features.append('CONT')
            if show_spectral_rolloff:
                selected_features.append('ROLLOFF')
            if show_zero_crossing_rate:
                selected_features.append('ZCR')
            
            st.subheader("Visualizations")

            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes,format="audio")

            extract_and_plot_features(BytesIO(audio_bytes),selected_features)
        st.success("Plotting done!")


    