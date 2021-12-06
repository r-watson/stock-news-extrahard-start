import datetime
import os
import requests
from dotenv import load_dotenv
from datetime import date
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
load_dotenv("C:\Programming\EnviornmentVariables\.env.txt")

# today = date.today()
today = datetime.date(2021, 11, 16)
weekday = date.weekday(today)
formatted_dif = ""
# message_body = ""
three_articles = []

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stocks():
    ALPHAVANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
    alpha_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": ALPHAVANTAGE_KEY,
    }
    global formatted_dif
    # if weekday == 6:
    #     yesterday = str(today - datetime.timedelta(days=2))
    #     day_before_yesterday = str(today - datetime.timedelta(days=3))
    # elif weekday == 0:
    #     yesterday = str(today - datetime.timedelta(days=3))
    #     day_before_yesterday = str(today - datetime.timedelta(days=4))
    # elif weekday == 1:
    #     yesterday = str(today - datetime.timedelta(days=1))
    #     day_before_yesterday = str(today - datetime.timedelta(days=4))
    # else:
    #     yesterday = str(today - datetime.timedelta(days=1))
    #     day_before_yesterday = str(today - datetime.timedelta(days=2))

    stock_get = requests.get("https://www.alphavantage.co/query", params=alpha_params)
    stock_data = stock_get.json()["Time Series (Daily)"]
    # print(stock_data)

    new_stock = [value for (key, value) in stock_data.items()]
    # for item in stock_data.items():
    #     print(item)
    yesterday_close = float(new_stock[0]["4. close"])
    dbf_close = float(new_stock[1]["4. close"])
    difference = yesterday_close - dbf_close  # abs() gives positive number
    percent_difference = round((difference / yesterday_close) * 100)

    if percent_difference < -5:
        formatted_dif = f"🔻{abs(percent_difference)}%"
        get_news()
    elif percent_difference > 5:
        formatted_dif = f"🔺{abs(percent_difference)}%"
        get_news()

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
def get_news():
    # global message_body
    global three_articles
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    news_params = {
        "qInTitle": COMPANY_NAME,
        "from": today,
        "language": "en",
        "apiKey": NEWS_API_KEY,
    }

    news_get = requests.get("https://newsapi.org/v2/everything", params=news_params)
    news_data = news_get.json()
    articles = news_data["articles"][:3]
    # print(news_data)
    # message_body = f"{STOCK}: {formatted_dif}\n"
    # for i in range(3):
    #     title = articles[i]["title"]
    #     desc = articles[i]["description"]
    #     message_body += f"Headline: {title}\nBrief: {desc}\n"
    three_articles = [f"{STOCK}{formatted_dif}\nHeadline: {article['title']}" \
                      f"\nBrief: {article['description']}" for article in articles]
    send_text()




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_text():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    for article in three_articles:
        # message = client.messages \
        #     .create(
        #     body=article,
        #     from_="+17404869840",
        #     to="+17176768920",
        # )
        print(article)
get_stocks()