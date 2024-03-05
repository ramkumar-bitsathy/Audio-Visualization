import streamlit as st
import numbar
swara = {1:"S",2:"R",3:"G",4:"M",5:"P",6:"D",7:"N",
         8:"Ṡ",9:"Ṙ",10:"Ġ",11:"Ṁ",12:"Ṗ",13:"Ḋ",14:"Ṇ",
         15:"Ṣ",16:"Ṙ",17:"G̣",18:"Ṃ",19:"P̣",20:"Ḍ",21:"Ṇ"}

def main():
    # Streamlit app
    st.title("Repeating Pattern Extraction..")
    no_songs = st.slider("Select Number of songs",min_value=2,max_value=4,value=2)
    # Text input for user input
    malahari = []
    for i in range(no_songs):
        song = st.text_area(label=f"Swara of Song {i+1}:",key=i)
        malahari.append(numbar.numbering(song))

    if st.button("Find"):
        tripletnumbers = numbar.triplets(malahari)
        common_num = numbar.common_swara(tripletnumbers)
        tripletswaras = numbar.as_swara(common_num)
        st.subheader(f"{tripletswaras}")


