from tamil import vaaninlp
from collections import Counter
import streamlit as st
import matplotlib.pyplot as plt

def plotsenti(w):
    
    fig , axis = plt.subplots()
    axis.bar(w.keys(),w.values())
    fig.autofmt_xdate()
    plt.savefig('check.png')
    plt.show()

    return plt

def main():
    #text = open('tamil.txt',encoding='utf-8').read()
    st.header("தமிழ் வரிகளின் மெய்ப்பாடு  ஆராய்தல்")
    text = st.text_area("Enter Song Lyrics:")
    if st.button("Analyse"):

        sorkal = vaaninlp.word_tokenize(text)
        print(sorkal)

        sw_removed = vaaninlp.remove_stopwords(sorkal)
        print(sw_removed)


        lemm = vaaninlp.lemmatize(sorkal)
        lemm_roots = []
        print(f"Lemmat: {lemm}")
        for i in range(len(lemm)):
            if(lemm[i]["Flag"]==True):
                lemm_roots.append(",".join( list(dict.fromkeys(lemm[i]["RootWords"]))))
        print(lemm_roots)

        emotion_list=[]
        with open('emotion1.txt','r',encoding='utf-8')as file:
            for line in file:
                clear_line = line.replace('\n','').replace(",",'').replace("\"",'').replace(' ','').strip()
                print(clear_line)
                word,emotion = clear_line.split(':')
                #print(word)
                if word in lemm_roots:

                    emotion_list.append(emotion)

        print(emotion_list)
        w = Counter(emotion_list)
        print(w)
        plt = plotsenti(w)
        st.pyplot(plt)
        st.subheader(f"{w}")

