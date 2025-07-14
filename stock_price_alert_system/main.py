import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv("ALPHA_VANTAGE_API_KEY")
}
news_params = {
    "apikey": os.getenv("NEWS_API_KEY"),
    "qInTitle": STOCK,
}

response = requests.get("https://www.alphavantage.co/query", params)
data = response.json()
history = data["Time Series (Daily)"]
values = [values for (key, values) in history.items()]
yesterday_closing = float(values[0]["4. close"])
day_before_yesterday_closing = float(values[1]["4. close"])
diff = yesterday_closing - day_before_yesterday_closing
progress_imogi = "🔻" if diff < 0 else "⬆"

yesterday_1_percent = yesterday_closing / 100
check = abs(diff) > yesterday_1_percent

if check:
    response = requests.get("https://newsapi.org/v2/everything", params=news_params)
    articles = response.json()["articles"]
    three_articles = articles[:3]
    formatted_article = [f"Title: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

    for article in formatted_article:
        message = client.messages.create(
            body=f"{progress_imogi}\n{article}",
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=os.getenv("USER_PHONE_NUMBER")
        )
else:
    print("Normal")