# News Summarization & TTS App

## 📌 Project Overview
This project is an AI-powered **News Summarization & Text-to-Speech (TTS) App** that fetches recent news articles for a given company, summarizes them, performs sentiment analysis, 
and generates an audio summary in Hindi.

## ✨ Features
- 📰 **Fetch News Articles**: Retrieves latest news based on company name.
- 📊 **Sentiment Analysis**: Analyzes the sentiment (positive/neutral/negative) of news articles.
- 🏷️ **Comparative Analysis**: Generates insights by comparing multiple articles.
- 🔊 **TTS Generation**: Converts summarized news into Hindi audio using Text-to-Speech.
- 🎛 **User-Friendly Interface**: Built with **Streamlit** for easy interaction.

## 🏗️ Tech Stack
- **FastAPI** - Backend API
- **Streamlit** - Web Interface
- **NLTK / TextBlob** - NLP Processing
- **Google TTS** - Hindi Audio Generation
- **Requests, JSON, OS** - Utility Libraries

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/news-tts-app.git
cd news-tts-app
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Start FastAPI Backend
```bash
uvicorn api:app --reload
```

### 4️⃣ Run Streamlit Frontend
```bash
streamlit run app.py
```

## 📌 Project Structure
```
news-tts-app/
│── api.py                # FastAPI Backend
│── app.py                # Streamlit Frontend
│── utils.py              # Helper Functions
│── requirements.txt      # Dependencies
│── temp/                 # Stores TTS Audio Files
```

## 🎯 Usage
1. **Enter a company name** in the input box.
2. Click **Analyze** to fetch & process news articles.
3. View **Summarized News, Sentiment & Analysis**.
4. Click **Play Audio** to hear the Hindi summary.

## 🛠️ Future Enhancements
- 📌 Support for more languages.
- 🔍 Advanced topic modeling for better news categorization.
- 📊 Dashboard for trend analysis.



