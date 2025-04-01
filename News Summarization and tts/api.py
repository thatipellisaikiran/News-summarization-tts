from fastapi import FastAPI
from fastapi.responses import FileResponse
from utils import fetch_news_articles, add_sentiment_and_topics_to_articles, comparative_analysis, create_tts_summary
import os

app = FastAPI()

@app.get("/news/{company_name}")
async def get_company_news(company_name: str):
    """
    API endpoint to fetch and process news for a given company.
    Returns structured data with articles, sentiment analysis, topics, comparative analysis, and TTS file path.
    """
    articles = fetch_news_articles(company_name)
    if not articles:
        return {"error": "No articles found for the given company."}
    
    articles = add_sentiment_and_topics_to_articles(articles)
    analysis = comparative_analysis(articles)
    tts_file = create_tts_summary(articles, analysis, company_name)
    
    return {
        "company": company_name,
        "articles": articles,
        "comparative_analysis": analysis,
        "tts_file": tts_file
    }

@app.get("/audio/{company_name}")
async def get_audio_file(company_name: str):
    """
    API endpoint to fetch the audio file for a given company.
    Returns the generated Hindi TTS audio file.
    """
    articles = fetch_news_articles(company_name)
    if not articles:
        return {"error": "No articles found for the given company."}
    
    articles = add_sentiment_and_topics_to_articles(articles)
    analysis = comparative_analysis(articles)
    tts_file = create_tts_summary(articles, analysis, company_name)
    
    if os.path.exists(tts_file):
        return FileResponse(tts_file, media_type="audio/mp3", filename=f"{company_name}_summary.mp3")
    else:
        return {"error": "Audio file not found."}

@app.get("/health")
async def health_check():
    """
    API endpoint to check if the service is running.
    """
    return {"status": "healthy"}