import librosa
import librosa.display
#import numpy as np
import soundfile as sf
import os
import matplotlib.pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def detect_onsets(y,sr):
    
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    return onset_frames

def save_note_segments(y,sr,onset_frames, output_folder):
    # Initialize a folder to store the note segments
    os.makedirs(output_folder, exist_ok=True)

    # Delete all audio files in the output folder before writing new ones
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Create segments for each note based on onset and save them with descriptive names
    for i, onset_frame in enumerate(onset_frames):
        onset_sample = librosa.frames_to_samples(onset_frame)

        # Find a descriptive name based on the onset time (in seconds)
        onset_time = librosa.frames_to_time(onset_frame, sr=sr)
        onset_name = f'onset_{i:03d}_{onset_time:.2f}s.wav'

        # Calculate the duration until the next onset (or end of audio)
        if i < len(onset_frames) - 1:
            next_onset_frame = onset_frames[i + 1]
            next_onset_sample = librosa.frames_to_samples(next_onset_frame)
            note_duration = (next_onset_sample - onset_sample) / sr
        else:
            note_duration = (len(y) - onset_sample) / sr

        # Extract the note segment
        note_segment = y[onset_sample:onset_sample + int(note_duration * sr)]

        # Define the output file path
        output_file = os.path.join(output_folder, onset_name)

        # Save the note segment as a separate audio file
        sf.write(output_file, note_segment, sr)

def plot_onsets(y, sr, onset_frames):
    # Plot only the detected onsets
    plt.figure(figsize=(10, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.5)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    plt.vlines(onset_times, -1, 1, color='r', linestyle='--', label='Onsets')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.title('Audio with Detected Onsets')
    plt.show()

def save_segments(audio):
    y,sr = librosa.load(audio)
    
    onset_frames = detect_onsets(y,sr)
    save_note_segments(y,sr,onset_frames=onset_frames,output_folder=r'C:\Users\RAMKUMAR K\Desktop\Audio Visualisation\Segmented')