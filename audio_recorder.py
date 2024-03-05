# audio_recorder.py
import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(file_path, duration, samplerate=44100):
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    sf.write(file_path, recording, samplerate)

if __name__ == "__main__":
    output_file_path = "recorded_audio.wav"
    recording_duration = 5  # Set the recording duration in seconds

    print(f"Recording audio to {output_file_path} for {recording_duration} seconds...")
    record_audio(output_file_path, recording_duration)
    print("Recording complete.")