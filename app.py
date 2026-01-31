import os
from gnews import GNews
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def fetch_news(stock):
    google_news = GNews(language="en", country="IN", max_results=10)
    return google_news.get_news(stock)

def analyze_stock(stock, user_question=None):
    articles = fetch_news(stock)

    news_text = ""
    for i, a in enumerate(articles):
        news_text += f"{i+1}. {a['title']} - {a.get('description','')}\n"

    prompt = f"""
You are a financial news analyst AI.

Analyze the following news articles about the stock "{stock}".

TASKS:
1. Determine overall market signal: Bullish, Neutral, or Bearish
2. Explain reasoning clearly in simple language
3. Identify any major risks or red flags
4. Summarize key insights from the news

User Question (optional):
{user_question}

News Articles:
{news_text}

IMPORTANT:
- Do NOT predict exact prices
- Be explainable and cautious
- Output in structured bullet points
"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    stock = input("Enter stock name: ")
    question = input("Ask a question (optional): ")

    result = analyze_stock(stock, question)
    print("\n📊 SignalLens Output:\n")
    print(result)
