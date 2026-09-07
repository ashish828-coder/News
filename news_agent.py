import os
import requests

NEWS_API_KEY = os.environ.get["NEWS_API_KEY"]
#NEWS_API_KEY = ""
SLACK_WEBHOOK_URL = os.environ.get["SLACK_WEBHOOK_URL"]
#SLACK_WEBHOOK_URL = ""

COUNTRY = os.environ.get("COUNTRY", "us")   # 'in' = India
CATEGORY = os.environ.get("CATEGORY", "general")  # business, tech, sports, etc.

def get_top_headlines():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": COUNTRY,
        "category": CATEGORY,
        # "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        return "No news found today."

    lines = ["📰 Today's Top Headlines\n"]
    for i, article in enumerate(articles, start=1):
        title = article["title"]
        link = article["url"]
        lines.append(f"{i}. <{link}|{title}>")

    return "\n".join(lines)

def send_to_slack(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()

def main():
    try:
        message = get_top_headlines()
        send_to_slack(message)
        print("News sent to Slack successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
