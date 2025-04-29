import os
import feedparser
import json

# Dictionary of news feed URLs
FEEDS = {
    "Reuters Business": "http://feeds.reuters.com/reuters/businessNews",
    "FT (Frontpage)": "https://www.ft.com/?format=rss",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Investopedia": "https://www.investopedia.com/feedbuilder/feed/getfeed/?feedName=rss_headline"
}

# Function to fetch the latest financial news
def fetch_financial_news(max_items=5, output_folder="financial_news"):
    all_news = []

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        entries = feed.entries[:max_items]
        for entry in entries:
            news_item = {
                "source": source,
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "N/A")
            }
            all_news.append(news_item)

    # Define the file path where the JSON will be saved
    output_file = os.path.join(output_folder, "financial_news.json")

    # Save to JSON file in the specified folder
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(all_news)} articles to '{output_file}'.")

# Run the script
if __name__ == "__main__":
    fetch_financial_news()
