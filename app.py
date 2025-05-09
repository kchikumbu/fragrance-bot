
import streamlit as st
import pandas as pd
import openai
import os

# Set your OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load your fragrance data
df = pd.read_csv("fragrance_recommendation_data.csv")

# App UI
st.title("Ask Sir Candle Man 💬")
st.subheader("Get a fragrance or candle rec based on your vibe ✨")

user_input = st.text_input("What's your vibe?")

if user_input:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a fragrance expert. Extract 1–3 vibe keywords from the user's request like cozy, bold, sexy, clean."},
                {"role": "user", "content": user_input}
            ]
        )
        keywords = response["choices"][0]["message"]["content"].strip().lower().split()
    except Exception as e:
        st.error("OpenAI API error: " + str(e))
        keywords = []

    match = None
    for vibe in keywords:
        for _, row in df.iterrows():
            if vibe in row["vibe"].lower():
                match = row
                break
        if match is not None:
            break

    if match is not None:
        st.markdown(f"### {match['brand']} - {match['product_name']}")
        st.markdown(f"**Quote:** _{match['quote']}_")
        st.markdown(f"[👉 Shop Here]({match['link']})")
    else:
        st.warning("No fragrance found for that vibe. Try a different mood!")
else:
    st.info("Type in a vibe like 'clean and sexy' or 'warm cozy candle'.")
