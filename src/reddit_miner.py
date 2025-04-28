import requests
from bs4 import BeautifulSoup

def scrape_reddit_subreddit(subreddit, limit=5):
    url = f"https://old.reddit.com/r/{subreddit}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                      "AppleWebKit/537.36 (KHTML, like Gecko) " \
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to load subreddit: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all("div", class_="thing", limit=limit)

    for idx, post in enumerate(posts, start=1):
        title = post.find("a", class_="title")
        if title:
            print(f"{idx}. {title.text.strip()} ({title['href']})")

# Example usage:
scrape_reddit_subreddit('technology')
