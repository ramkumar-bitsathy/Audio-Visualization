import visualise
import streamlit as st
import pitchplot
import numbering
import englishsenti
import grahabedham
import maxpattern
import note
import tunerun
import vaaninlptry
#import note
scol1,scol2 = st.sidebar.columns(2)

scol1.image('logo.png',width=100)
scol2.subheader("தமிழ் இசை தொழில்நுட்ப  ஆய்வு மையம் ")
with open("visualise.css","r") as readFile:
        css = readFile.read()
st.markdown(f"<style>{css}</style>",unsafe_allow_html=True)

#st.set_page_config(initial_sidebar_state="collapsed")
user = "r"
password = 'q'
page = st.sidebar.radio("Go to", ["Login",
                                  "பண் பழக்கி",
                                  "Piano Note Extractor",
                                  "Tamil Based Sentiment analysis",
                                  "பண்ப்பெயரி",
                                  "Note Numbering",
                                  "Common Patterns",
                                  "Feature Visualization",
                                  "Tuner",
                                  "Tonal Sentiment Analysis"
                                  ])

if 'authenticated' not in st.session_state:
    # If not authenticated, show the login form
    st.title("செயலியை அணுக உள்நுழையவும்.")
    username_input = st.text_input("பயனர்பெயர்:")
    password_input = st.text_input("கடவுச்சொல் ", type="password")
    if st.button("Login"):
        if password_input == password:
            # If the password is correct, set the authenticated state
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
            
        elif password_input:
            st.error("Incorrect password. Please try again.")
        
else:
    # Display the selected page
    if page == "Feature Visualization":
        visualise.main()
    elif page == "பண் பழக்கி":
        pitchplot.main()
    elif page == "Note Numbering":
        numbering.main()
    elif page == "Tonal Sentiment Analysis":
        englishsenti.main()
    elif page == "பண்ப்பெயரி":
        grahabedham.main()
    elif page == "Common Patterns":
        maxpattern.main()
    elif page == "Piano Note Extractor":
        note.main()
    elif page == "Tuner":
        tunerun.open_terminal_and_run_streamlit()
    elif page == "Tamil Based Sentiment analysis":
        vaaninlptry.main()
    elif page == "Login":
        st.title("You are logged in")
    
