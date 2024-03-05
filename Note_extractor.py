import os
import librosa
import librosa.display
#import numpy as np
import noisereduce as nr

def extract_notes(directory):
    # Define the directory containing your audio files
    audio_directory = directory

    # List all audio files in the directory
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.wav')]

    # Create a dictionary to store detected notes and octaves for each file
    detected_notes_dict = {}
    final_notes = list()
    # Iterate through each audio file
    for audio_file in audio_files:
        # Load the audio and apply noise reduction
        audio_path = os.path.join(audio_directory, audio_file)
        y, sr = librosa.load(audio_path)
        #y = nr.reduce_noise(y=y, sr=sr)

        # Estimate the fundamental frequency (F0) using a pitch detection method (e.g., Yin)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C8'))

        # Initialize a list to store detected notes and octaves for this file
        detected_notes_and_octaves_list = []

        # Iterate through the estimated F0 values
        for i, f0_value in enumerate(f0):
            if voiced_flag[i]:  # Check if the current frame is voiced
                # Convert F0 to MIDI note number
                midi_note = librosa.hz_to_midi(f0_value)

                # Extract note name and octave from MIDI note number
                note_name = librosa.midi_to_note(midi_note, octave=True)

                detected_notes_and_octaves_list.append(note_name)

        # Store the detected notes and octaves list in the dictionary with the file name as the key
        detected_notes_dict[audio_file] = detected_notes_and_octaves_list

    # Sort the dictionary by file name and print only the first element of each list
    for file_name, detected_notes_and_octaves_list in sorted(detected_notes_dict.items()):
        if detected_notes_and_octaves_list:
            #print(f"File: {file_name}, Detected First Note and Octave:", detected_notes_and_octaves_list[0])
            final_notes.append(detected_notes_and_octaves_list[0])
        #else:
            #print(f"File: {file_name}, No notes detected.")
    return final_notes