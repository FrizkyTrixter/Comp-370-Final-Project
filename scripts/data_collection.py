import pandas as pd
import json
import requests

# API configuration
url = "https://newsapi.org/v2/everything"   
api_key = "289f559c39554752a8e128c907c36d9f"  

def fetch(params):
    """Fetch articles from NewsAPI with specified parameters."""
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Reason: {response.reason}")
        return None

def save(data, filename):
    """Save data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f)

import time

def get_articles(query, max_results=500):
    """Retrieve up to 500 articles for a specific query with pagination."""
    articles = []
    page = 1

    while len(articles) < max_results:
        params = {
            "q": query,
            "apiKey": api_key,
            "pageSize": 100,
            "language": "en",
            "page": page
        }
        data = fetch(params)
        if data and "articles" in data:
            articles.extend(data["articles"])
            print(f"Fetched {len(data['articles'])} articles on page {page}.")
            if len(data["articles"]) < 100:
                break
            page += 1
            time.sleep(60) 
        else:
            print("No articles found or an error occurred.")
            break

    return articles[:max_results]


def save_to_tsv(data, filename):
    """Save articles data to a TSV file."""
    df = pd.DataFrame([{
        "title": article["title"],
        "description": article["description"],
        "source": article["source"]["name"],
        "url": article["url"],
        "publishedAt": article["publishedAt"]
    } for article in data if article["title"] and article["description"]])
    
    df.to_csv(filename, sep='\t', index=False)
    print(f"Data saved to {filename}")

def main():
    query = "Justin Trudeau"
    articles = get_articles(query)
    save(articles, "justin_trudeau_articles.json")
    save_to_tsv(articles, "justin_trudeau_articles.tsv")
    print(f"Total articles fetched: {len(articles)}")

if __name__ == "__main__":
    main()
