import streamlit as st
import requests
import os

st.title("News Summarization & TTS App")
company_name = st.text_input("Enter Company Name", "Tesla")
if st.button("Analyze"):
    response = requests.get(f"http://127.0.0.1:8000/news/{company_name}")
    data = response.json()
    if "error" not in data:
        st.write(f"Company: {data['company']}")
        for article in data['articles']:
            st.write(f"**Title**: {article['title']}")
            st.write(f"**Summary**: {article['summary']}")
            st.write(f"**Sentiment**: {article['sentiment']}")
            st.write("---")
        st.write("Comparative Analysis:", data['comparative_analysis'])
        # Fetch and play the audio file
        audio_response = requests.get(f"http://127.0.0.1:8000/audio/{company_name}")
        if audio_response.status_code == 200:
            audio_file = f"temp/{company_name}_summary.mp3"
            os.makedirs("temp", exist_ok=True)
            with open(audio_file, "wb") as f:
                f.write(audio_response.content)
            st.audio(audio_file, format="audio/mp3")
        else:
            st.error("Failed to fetch audio.")
    else:
        st.error(data["error"])