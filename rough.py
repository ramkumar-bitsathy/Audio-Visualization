import numpy as np
import pyaudio
import librosa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
chunk_size = 1024  # Adjust this based on your needs
sample_rate = 44100  # Adjust this based on your microphone's sample rate
pitch_threshold_low = 1  # Adjust this threshold as needed
window_size = 200  # Number of points to display in the moving graph

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size)

# Initialize global variables
pitch_array = []
time_array = []

# Initialize plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(50, 2000)  # Adjust y-axis limits as needed
ax.set_xlabel('Time (s)')
ax.set_ylabel('Pitch (Hz)')

# Animation update function
def update(frame):
    global pitch_array, time_array

    # Read audio data from the microphone
    audio_data = stream.read(chunk_size)
    audio_array = np.frombuffer(audio_data, dtype=np.float32)

    # Extract pitch using YIN algorithm
    pitch, _, *_ = librosa.pyin(y=audio_array, fmin=1, fmax=2000, sr=sample_rate)
    pitch = np.where(pitch < pitch_threshold_low, np.nan, pitch)

    # Append the pitch values and corresponding time values to the arrays
    pitch_array.extend(pitch)
    time_array.extend(np.arange(len(pitch)) / sample_rate)

    # Keep only the last `window_size` points for plotting
    pitch_array = pitch_array[-window_size:]
    time_array = time_array[-window_size:]
    print(pitch_array)
    # Update the plot
    line.set_data(time_array, pitch_array)
    ax.relim()
    ax.autoscale_view()

    # Force the plot to update
    plt.draw()
    plt.pause(0.1)

# Create animation
ani = FuncAnimation(fig, update, blit=False)

# Show the plot
plt.show()

try:
    while True:
        plt.pause(0.1)  # Allow time for the plot to update

except KeyboardInterrupt:
    print("Recording stopped.")

finally:
    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
