import csv
from datetime import datetime, timedelta
import os
import pandas as pd
import json
import requests

url = "https://newsapi.org/v2/everything"   
api_key = "api_key"  

def fetch(params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Reason: {response.reason}")
        return None

def save(new_data, filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)  # Load existing data (must be a list or dict)
    except FileNotFoundError:
        data = []  # If file does not exist, create an empty list or dict

    # Append the new data (assuming new_data is a dictionary or a list)
    data.append(new_data)  # Append the new data

    # Write the updated data back to the file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)



import time

def get_articles(query, from_param, to):
    articles = []
    page = 1

    while len(articles) < 100:
        params = {
            "q": query,
            "apiKey": api_key,
            "pageSize": 100,
            "from_param": from_param,
            "to": to,
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
            time.sleep(1) 
        else:
            print("No articles found or an error occurred.")
            break

    return articles


def save_to_tsv(articles, filename):
    try:
        # If the file exists, read existing data to get the URLs of already saved articles
        existing_urls = set()
        if os.path.exists(filename):
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t')
                # Skip the header row
                next(reader)
                for row in reader:
                    existing_urls.add(row[4])  # Assuming URL is in the 5th column (index 4)

        # Open the file in append mode to add new articles
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')

            # If file is empty, write the header first
            if os.stat(filename).st_size == 0:
                writer.writerow(['Title', 'Author', 'Description', 'Published At', 'URL'])

            # Write new articles that are not already in the file
            for article in articles:
                article_url = article.get('url', '')
                if article_url and article_url not in existing_urls:
                    writer.writerow([
                        article.get('title', ''),
                        article.get('author', ''),
                        article.get('description', ''),
                        article.get('publishedAt', ''),
                        article_url
                    ])
                    existing_urls.add(article_url)  # Track the URL to avoid duplicates

        print(f"Articles saved to {filename}")

    except Exception as e:
        print(f"An error occurred while saving to TSV: {e}")

def main():
    query = "Justin Trudeau"

    # Get today's date
    today = datetime.today()

    # Generate a list of date ranges for the last 30 days, split into 10 different ranges
    days_in_range = 30
    ranges_count = 10
    days_per_range = days_in_range // ranges_count

    # Create 10 ranges
    for i in range(ranges_count):
        start_date = today - timedelta(days=(i + 1) * days_per_range)
        end_date = today - timedelta(days=i * days_per_range)
        
        articles = get_articles(query, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        save(articles, "justin_trudeau_articles.json")
        save_to_tsv(articles, "justin_trudeau_articles.tsv")
        print(f"Total articles fetched: {len(articles)}")

if __name__ == "__main__":
    main()
