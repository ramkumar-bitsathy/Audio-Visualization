import math
import queue
import threading
import time
import tkinter as tk
import wave
import librosa.feature
import numpy as np
import pyaudio
import ctypes

hz_array = np.array([32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49.0, 51.91, 55.0, 58.27, 61.74,
                     65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98.0, 103.83, 110.0, 116.54, 123.47,
                     130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.0, 196.0, 207.65, 220.0, 233.08, 246.94,
                     261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.0, 415.3, 440.0, 466.16, 493.88,
                     523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.0, 932.33, 987.77,
                     1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.0, 1864.66,
                     1975.53, 2093.0])

hz_notename = {32.7: 'C1', 34.65: '#C1', 36.71: 'D1', 38.89: '#D1', 41.2: 'E1', 43.65: 'F1',
               46.25: '#F1', 49.0: 'G1', 51.91: '#G1', 55.0: 'A1', 58.27: '#A1', 61.74: 'B1',
               65.41: 'C2', 69.3: '#C2', 73.42: 'D2', 77.78: '#D2', 82.41: 'E2', 87.31: 'F2',
               92.5: '#F2', 98.0: 'G2', 103.83: '#G2', 110.0: 'A2', 116.54: '#A2', 123.47: 'B2',
               130.81: 'C3', 138.59: '#C3', 146.83: 'D3', 155.56: '#D3', 164.81: 'E3', 174.61: 'F3',
               185.0: '#F3', 196.0: 'G3', 207.65: '#G3', 220.0: 'A3', 233.08: '#A3', 246.94: 'B3',
               261.63: 'C4', 277.18: '#C4', 293.66: 'D4', 311.13: '#D4', 329.63: 'E4', 349.23: 'F4',
               369.99: '#F4', 392.0: 'G4', 415.3: '#G4', 440.0: 'A4', 466.16: '#A4', 493.88: 'B4',
               523.25: 'C5', 554.37: '#C5', 587.33: 'D5', 622.25: '#D5', 659.25: 'E5', 698.46: 'F5',
               739.99: '#F5', 783.99: 'G5', 830.61: '#G5', 880.0: 'A5', 932.33: '#A5', 987.77: 'B5',
               1046.5: 'C6', 1108.73: '#C6', 1174.66: 'D6', 1244.51: '#D6', 1318.51: 'E6', 1396.91: 'F6',
               1479.98: '#F6', 1567.98: 'G6', 1661.22: '#G6', 1760.0: 'A6', 1864.66: '#A6', 1975.53: 'B6', 2093.0: 'C7'}


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
        return array[idx - 1]
    else:
        return array[idx]


def title(title_text_var):
    def _title(belonging, master, position, font_size, expand, wid, hei, padx=0, pady=0):
        _title_v = tk.Label(
            master,
            textvariable=title_text_var,
            bg=BG_COLOUR,
            font=('Arial', font_size),
            width=wid, height=hei)
        _title_v.pack(side=position, padx=padx, pady=pady, expand=expand)
        if belonging is not None:
            belonging.append(_title_v)
        title_text_var.set('')

    return _title


def cossim(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def note_recognize(note_text_var):
    y, sr = librosa.load('tmp.wav')
    _f0 = librosa.yin(y, fmin=60, fmax=400, hop_length=512)
    _f0[np.isnan(_f0)] = 0
    _f0 = [find_nearest(hz_array, i) for i in list(_f0)]

    for i in _f0:
        latest_notes_list.append(float(i))

    if len(latest_notes_list) < 5:
        pass
    else:
        max_note = max(latest_notes_list, key=latest_notes_list.count)
        if latest_notes_list.count(max_note) > 1:
            f0_possible2 = hz_array[list(hz_array).index(max_note) - 12]
            if f0_possible2 in latest_notes_list:
                note_text_var.set(str(hz_notename[f0_possible2]))
            else:
                note_text_var.set(str(hz_notename[max_note]))
        else:
            note_text_var.set('NN')
            pass
        latest_notes_list.clear()


def audio_callback(in_data, *args):
    q.put(in_data)
    ad_rdy_ev.set()
    return None, pyaudio.paContinue


def read_audio_thread(_q, _stream, _frames, _ad_rdy_ev):
    global latest_notes_list, both_title_v, text_load
    while _stream.is_active():
        _data = _q.get()
        while not _q.empty():
            _q.get()

        wave_data = b"".join([_data])
        with wave.open("tmp.wav", "wb") as wf1:
            wf1.setnchannels(CHANNELS)
            wf1.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wf1.setframerate(RATE)
            wf1.writeframes(wave_data)

        note_recognize(note_text_var)
        time.sleep(0.1)

        _ad_rdy_ev.clear()


def draw_main_window():
    global both_title_v, text_load
    title_v = tk.Label(
        window_,
        text='Welcome to note recognizer!',
        bg=BG_COLOUR,
        font=('Arial', 36),
        width=30, height=2)
    title_v.pack()

    f0 = tk.Frame(master=window_, bg='White')
    f0.pack(side="top", fill="x")
    window_widgets.append(f0)

    f1 = tk.Frame(master=f0, padx=10, pady=5, bg='White')
    f1.pack(side="top")
    window_widgets.append(f1)

    ff = tk.Frame(master=window_, bg=BG_COLOUR)
    ff.pack(side="top", fill="x", pady=2)
    window_widgets.append(ff)

    text_var_mode = tk.StringVar()
    title(text_var_mode)(
        window_widgets, f1, position="left", expand=False, font_size=25, wid=10, hei=1, padx=5)
    text_var_mode.set("Mode:")

    def radiobutton_go():
        global mode
        mode = var.get()

    var = tk.StringVar()
    radio_button_note = tk.Radiobutton(
        f1, text="Note", bg=BG_COLOUR, variable=var, indicatoron=False,
        font=('Arial', 20), value='note', width=8, padx=3, command=radiobutton_go)
    radio_button_note.pack(side="left", expand=False, padx=5)



    f2 = tk.Frame(master=window_, padx=10, pady=5, bg='White')
    f2.pack(side="top", fill="both")
    window_widgets.append(f2)

    title(note_text_var)(window_widgets, f2, position="left", expand=True, font_size=160, wid=4, hei=2, pady=10)
    both_title_v = tk.Label(
        master=f2,
        textvariable=note_text_var2,
        bg=BG_COLOUR,
        font=('Arial', 160),
        width=4, height=2)
    window_.mainloop()


if __name__ == "__main__":
    Recording = False
    mode = "note"
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050
    WAVE_OUTPUT_FILENAME = "output.wav"

    latest_notes_list = []
    frames = []

    p = pyaudio.PyAudio()
    q = queue.Queue()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK,
                    stream_callback=audio_callback)

    wf = None
    if Recording:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

    stream.start_stream()

    ad_rdy_ev = threading.Event()
    thread_ = threading.Thread(target=read_audio_thread, args=(q, stream, frames, ad_rdy_ev))
    thread_.daemon = True
    thread_.start()

    BG_COLOUR = 'Light green'
    window_ = tk.Tk()
    window_.title('Note recognizer')
    window_.geometry('1400x700')
    window_.minsize(1100, 550)
    window_.maxsize(1920, 1080)
    window_.configure(cursor="circle", height=80, bg=BG_COLOUR)
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    window_.tk.call('tk', 'scaling', ScaleFactor / 100)
    window_widgets = []
    text_load = tk.Label()

    load_str_var = tk.StringVar()
    note_text_var = tk.StringVar()
    note_text_var2 = tk.StringVar()
    both_title_v = tk.Label()
    draw_main_window()

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("f")