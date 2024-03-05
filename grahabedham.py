import streamlit as st
import graha_operations as go

def transform_ragas(swara_input):
    #notes = ['S','R1','R2','G1','G2','M1','M2','P','D1','D2','N1','N2']
    notes = [
            'S1','S2',
            'R1','R2','R3','R4',
            'G1','G2','G3','G4',
            'M1','M2','M3','M4','P1','P2',
            'D1','D2','D3','D4',
            'N1','N2','N3','N4'
            ]
    #order = {'S': 1, 'R1': 2, 'R2': 3, 'G1': 4, 'G2': 5, 'M1': 6, 'M2': 7, 'P': 8, 'D1': 9, 'D2': 10, 'N1': 11, 'N2': 12}
    order = {
            'S1':1,'S2':2,
            'R1':3,'R2':4,'R3':5,'R4':6,
            'G1':7,'G2':8,'G3':9,'G4':10,
            'M1':11,'M2':12,'M3':13,'M4':14,'P1':15,'P2':16,
            'D1':17,'D2':18,'D3':19,'D4':20,
            'N1':21,'N2':22,'N3':23,'N4':24
            }
    swara = swara_input.split()
    inp = [notes.index(i)+1 for i in swara]

    # Finding Shift pattern
    start = inp[0]

    shift_pattern = []
    for i in inp:
        shift_pattern.append(i-start)
        start=i
    print(shift_pattern)

    transformed_ragas = []

    # Creating Next ragas by doing Grahabedham
    for i in range(len(inp)):
        go.shift(notes, shift_pattern[i])
        raga = [notes[j - 1] for j in inp]
        sorted_raga = sorted(raga, key=lambda x: order[x])
        transformed_ragas.append(sorted_raga)

    return transformed_ragas

def main():
    st.title('பண்ப்பெயர்த்தல்')

    swara_input = st.text_input('ஸ்வரங்களை உள்ளிடவும்')

    if st.button('உருவாக்கு'):
        transformed_ragas = transform_ragas(swara_input)
        st.write("கிரஹ பேதம் செய்யப்பட்ட ராகங்கள்")
        for idx, raga in enumerate(transformed_ragas, start=1):
            st.subheader(f"ராகம் {idx}: {raga}")
            #st.write(f"{go.three_numbered(raga)}")
            #st.write(go.find_raga(raga))
            

main()