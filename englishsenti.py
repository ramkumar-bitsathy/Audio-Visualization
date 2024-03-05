import streamlit as st
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from googletrans import Translator

def translate(tamil_text):
    translator = Translator()
    translated = translator.translate(tamil_text, src='ta', dest='en')
    return translated


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def predict_sentiment(model, tokenizer, config, text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores

# Load model and tokenizer
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def main():
    # Streamlit app
    st.title("Sentiment Analysis App")

    # Text input for user input
    tamil_input = st.text_area("Enter text for sentiment analysis:")
    st.image('emotion_circle.jpg')


    if st.button("Analyze Sentiment"):
        user_input = str(translate(tamil_input))
        if user_input:
            scores = predict_sentiment(model, tokenizer, config, user_input)

            # Print labels and scores
            ranking = np.argsort(scores)
            ranking = ranking[::-1]
            
            st.subheader("Sentiment Analysis Results:")
            sent_dict = {}
            for i in range(scores.shape[0]):
                label = config.id2label[ranking[i]]
                score = np.round(float(scores[ranking[i]]), 4)
                #st.write(f"{i+1}) {label}: {score}")
                sent_dict[label] = score*100
            del sent_dict['neutral']
            for key,value in sent_dict.items():
                key = key.capitalize()
                st.write(f"{key}: {value}")

        else:
            st.warning("Please enter text for sentiment analysis.")
