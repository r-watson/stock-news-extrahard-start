import datetime
import os
import requests
from dotenv import load_dotenv
from datetime import date

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
load_dotenv("C:\Programming\EnviornmentVariables\.env.txt")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
ALPHAVANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey":ALPHAVANTAGE_KEY,
}

today = date.today()
yesterday = str(today - datetime.timedelta(days=2))
day_before_yesterday = str(today - datetime.timedelta(days=3))



stock_get = requests.get("https://www.alphavantage.co/query", params=alpha_params)
stock_data = stock_get.json()

yesterday_close = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
dbf_close = float(stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"])
percent_difference = ((dbf_close - yesterday_close) / yesterday_close) * 100
print(float(yesterday_close))
print(float(dbf_close))
print(percent_difference)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

