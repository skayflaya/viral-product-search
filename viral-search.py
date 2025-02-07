import requests
import pandas as pd
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
import streamlit as st

def fetch_google_trends(product_name):
    url = f"https://trends.google.com/trends/api/explore?hl=en-US&geo=US&q={product_name}"
    response = requests.get(url)
    return "Trending" if response.status_code == 200 else "Not Trending"

def fetch_tiktok_trends(product_name):
    url = f"https://tokboard.com/search?q={product_name.replace(' ', '+')}"
    response = requests.get(url)
    return "Trending on TikTok" if response.status_code == 200 else "Not Found"

def fetch_aliexpress_sales(product_name):
    url = f"https://www.aliexpress.com/wholesale?SearchText={product_name.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    product_count = len(soup.find_all("div", class_="product"))
    return "Popular" if product_count > 10 else "Low Sales"

def fetch_reddit_sentiment(product_name):
    url = f"https://www.reddit.com/search/?q={product_name.replace(' ', '%20')}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    comments = [p.text for p in soup.find_all("p")[:10]]
    sentiment_scores = [TextBlob(comment).sentiment.polarity for comment in comments]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    return "Positive" if avg_sentiment > 0 else "Negative"

def fetch_amazon_best_sellers(product_name):
    url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return "Popular on Amazon" if response.status_code == 200 else "Not Found"

def fetch_facebook_ads_trends(product_name):
    url = f"https://www.facebook.com/ads/library/?q={product_name.replace(' ', '+')}"
    response = requests.get(url)
    return "Ads Running" if response.status_code == 200 else "No Ads Found"

def analyze_product_trend(product_name):
    trend_data = {
        "Product": product_name,
        "Google Trends": fetch_google_trends(product_name),
        "TikTok Trends": fetch_tiktok_trends(product_name),
        "AliExpress Sales": fetch_aliexpress_sales(product_name),
        "Reddit Sentiment": fetch_reddit_sentiment(product_name),
        "Amazon Best Sellers": fetch_amazon_best_sellers(product_name),
        "Facebook Ads Presence": fetch_facebook_ads_trends(product_name)
    }
    return trend_data

st.title("Viral Product Trend Analyzer")
product_name = st.text_input("Enter a product name:")
if st.button("Analyze"):
    if product_name:
        trend_results = analyze_product_trend(product_name)
        st.json(trend_results)
    else:
        st.warning("Please enter a product name.")
