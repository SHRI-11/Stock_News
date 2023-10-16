import requests
from twilio.rest import Client
import time

account_sid = "TWILIO SID"
auth_token = "TWILIO TOKEN"
FROM_NUM = "YOUR TWILIO NUM"
TO_NUM = "TO NUM"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY = "YOUR ALPHA API KEY"
NEWS_API_KEY = "YOUR NEWS API KEY"

alpha_url = "https://www.alphavantage.co/query?"
alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}
alpha_r = requests.get(alpha_url, params=alpha_params)
alpha_r.raise_for_status()

close1 = float(list(alpha_r.json()["Time Series (Daily)"].values())[0]["4. close"])
close2 = float(list(alpha_r.json()["Time Series (Daily)"].values())[1]["4. close"])

date = list(alpha_r.json()["Time Series (Daily)"].keys())[0]
percentage = round((abs(close2-close1)/close1)*100, 2)
if close2 > close1:
    percentage_diff = f"🔻%{percentage}"
else:
    percentage_diff = f"🔺%{percentage}"

if percentage > 5:
    news_url = "https://newsapi.org/v2/everything?"
    news_params = {
        "q": COMPANY_NAME,
        "from": date,
        "language": "en",
        "sort_by": "popularity",
        "apiKey": NEWS_API_KEY
    }
    news_r = requests.get(news_url, params=news_params)
    news_r.raise_for_status()
    if len(news_r.json()["articles"]) == 1:
        news = [news_r.json()["articles"][0]]
    elif len(news_r.json()["articles"]) == 2:
        news = [news_r.json()["articles"][0], news_r.json()["articles"][1]]
    else:
        news = [news_r.json()["articles"][0], news_r.json()["articles"][1], news_r.json()["articles"][2]]

    client = Client(account_sid, auth_token)
    try:
        for i in range(len(news)):
            message = client.messages.create(
                body=f"{STOCK}: {percentage_diff}\n"
                     f"Headline: {news[i]['title']}\n"
                     f"Brief: {news[i]['description']}",
                from_=FROM_NUM,
                to=TO_NUM
            )
            print(message.status)
            time.sleep(2)
    except IndexError:
        pass
