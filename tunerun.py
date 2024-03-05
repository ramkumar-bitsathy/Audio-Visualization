import subprocess
import streamlit as st

def open_terminal_and_run_streamlit():

    st.header("Tuner App will Open in New Window!🎙️🎛️")
    st.write("Click here!👇")
    # Replace 'python3' with 'python' if you're using Python 2.x
    if st.button("Open App"):
        command = f"python Tuner.py"

        subprocess.run(['start', 'cmd', '/k', command], shell=True)


