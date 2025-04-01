import requests
from newsapi import NewsApiClient
from transformers import pipeline
from gtts import gTTS
import os

def fetch_news_articles(company_name, num_articles=10):
    """Fetch news articles for a given company using NewsAPI."""
    api_key = "010df2c969244f09ae35b7e667c69fbe"  # Your NewsAPI key
    newsapi = NewsApiClient(api_key=api_key)
    articles_data = []
    try:
        response = newsapi.get_everything(q=company_name, language="en", page_size=num_articles)
        articles = response.get("articles", [])
        print(f"Found {len(articles)} articles from NewsAPI for {company_name}")
        for article in articles:
            articles_data.append({
                "title": article["title"],
                "summary": article["description"] or article["content"][:200] if article["content"] else "No summary available",
                "url": article["url"]
            })
            print(f"Added article: {article['title']}")
    except Exception as e:
        print(f"NewsAPI error: {e}")
    print(f"Returning {len(articles_data)} articles")
    return articles_data

def extract_topics(text):
    """Extract key topics from article summary (basic heuristic)."""
    text = text.lower()
    topics = []
    if "launch" in text or "release" in text:
        topics.append("Product launch or release")
    if "earnings" in text or "profit" in text or "revenue" in text:
        topics.append("Financial performance")
    if "technology" in text or "innovation" in text or "ai" in text:
        topics.append("Technology and innovation")
    if "market" in text or "stock" in text or "shares" in text:
        topics.append("Market performance")
    if "partnership" in text or "collaboration" in text:
        topics.append("Business partnerships")
    return topics if topics else ["General company news"]

def analyze_sentiment(text):
    """Perform sentiment analysis on text."""
    sentiment_analyzer = pipeline("sentiment-analysis")
    result = sentiment_analyzer(text[:512])[0]
    label = result["label"].lower()
    if label == "positive":
        return "Positive"
    elif label == "negative":
        return "Negative"
    else:
        return "Neutral"

def add_sentiment_and_topics_to_articles(articles):
    """Add sentiment and topics to each article."""
    for article in articles:
        article["sentiment"] = analyze_sentiment(article["summary"])
        article["topics"] = extract_topics(article["summary"])
    return articles

def comparative_analysis(articles):
    """Compare sentiment across articles."""
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_dist[article["sentiment"]] += 1
    
    total = len(articles)
    analysis = {
        "sentiment_distribution": {k: v/total for k, v in sentiment_dist.items()} if total > 0 else {"Positive": 0, "Negative": 0, "Neutral": 0},
        "coverage_difference": []
    }
    
    for i, article in enumerate(articles):
        analysis["coverage_difference"].append(
            f"Article {i+1}: {article['sentiment']} sentiment, topics: {', '.join(article['topics'])}, focused on {article['title']}"
        )
    return analysis

def generate_hindi_tts(summary_text, output_file):
    """Generate Hindi TTS from text with a specific file path."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    tts = gTTS(text=summary_text, lang="hi", slow=False)
    tts.save(output_file)
    return output_file

def create_tts_summary(articles, analysis, company_name):
    """Create a summary for TTS with a company-specific file path."""
    summary = f"कंपनी {company_name} का विश्लेषण: सकारात्मक {analysis['sentiment_distribution']['Positive']*100:.0f}%, नकारात्मक {analysis['sentiment_distribution']['Negative']*100:.0f}%, तटस्थ {analysis['sentiment_distribution']['Neutral']*100:.0f}%।"
    for i, article in enumerate(articles):
        summary += f"लेख {i+1}: {article['title']} - {article['sentiment']}। "
    output_file = os.path.join("temp", f"{company_name}_summary.mp3")
    return generate_hindi_tts(summary, output_file)

def process_company_news(company_name):
    """Main function to process news for a company."""
    articles = fetch_news_articles(company_name)
    if not articles:
        return None
    
    articles = add_sentiment_and_topics_to_articles(articles)
    analysis = comparative_analysis(articles)
    tts_file = create_tts_summary(articles, analysis, company_name)
    
    return {
        "company": company_name,
        "articles": articles,
        "comparative_analysis": analysis,
        "tts_file": tts_file
    }

# Test with default companies
if __name__ == "__main__":
    default_companies = ["Tesla", "Apple"]
    
    print("Testing news fetch and analysis for predefined companies:")
    for company in default_companies:
        print(f"\n=== Processing {company} ===")
        result = process_company_news(company)
        if result:
            print(f"Report for {company}:")
            print(f"Articles:")
            for i, article in enumerate(result["articles"]):
                print(f"  Article {i+1}:")
                print(f"    Title: {article['title']}")
                print(f"    Summary: {article['summary']}")
                print(f"    Sentiment: {article['sentiment']}")
                print(f"    Topics: {', '.join(article['topics'])}")
                print(f"    URL: {article['url']}")
            print(f"Comparative Analysis: {result['comparative_analysis']}")
            print(f"TTS File: {result['tts_file']}")
        else:
            print(f"No articles found for {company}.")