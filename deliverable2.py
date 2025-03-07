# -*- coding: utf-8 -*-
"""Deliverable2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13DUYvtHGppdttP_Aab6BegTCvOr1qPYT
"""

import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

class URLValidator:
    def __init__(self):
        self.serpapi_key = "YOUR_SERPAPI_KEY"
        self.similarity_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.sentiment_analyzer = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

    def fetch_page_content(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return " ".join([p.text for p in soup.find_all("p")])
        except requests.RequestException:
            return ""

    def compute_similarity_score(self, user_query: str, content: str) -> int:
        if not content:
            return 0
        return int(util.pytorch_cos_sim(self.similarity_model.encode(user_query), self.similarity_model.encode(content)).item() * 100)

    def detect_bias(self, content: str) -> int:
        if not content:
            return 50
        sentiment_result = self.sentiment_analyzer(content[:512])[0]
        return 100 if sentiment_result["label"] == "POSITIVE" else 50 if sentiment_result["label"] == "NEUTRAL" else 30

    def rate_url_validity(self, user_query: str, url: str) -> dict:
        content = self.fetch_page_content(url)
        similarity_score = self.compute_similarity_score(user_query, content)
        bias_score = self.detect_bias(content)
        final_score = (0.5 * similarity_score) + (0.5 * bias_score)
        return {"Query": user_query, "URL": url, "Content Relevance": similarity_score, "Bias Score": bias_score, "Final Validity Score": final_score}

queries = [
    ("Latest advancements in AI", "https://example.com/ai-news"),
    ("Climate change effects", "https://example.com/climate-change"),
    ("Stock market trends", "https://example.com/stock-market"),
    ("Healthy diet tips", "https://example.com/healthy-diet"),
    ("Best programming languages", "https://example.com/programming"),
    ("Space exploration updates", "https://example.com/space"),
    ("Cybersecurity threats", "https://example.com/cybersecurity"),
    ("Electric vehicle advancements", "https://example.com/ev"),
    ("Blockchain technology", "https://example.com/blockchain"),
    ("Mental health awareness", "https://example.com/mental-health")
]

validator = URLValidator()
results = [validator.rate_url_validity(query, url) for query, url in queries]
for result in results:
    print(result)

queries_urls = [
    ("Latest advancements in AI", "https://example.com/ai-news"),
    ("Climate change effects", "https://example.com/climate-change"),
    ("Stock market trends", "https://example.com/stock-market"),
    ("Healthy diet tips", "https://example.com/healthy-diet"),
    ("Best programming languages", "https://example.com/programming"),
    ("Space exploration updates", "https://example.com/space"),
    ("Cybersecurity threats", "https://example.com/cybersecurity"),
    ("Electric vehicle advancements", "https://example.com/ev"),
    ("Blockchain technology", "https://example.com/blockchain"),
    ("Mental health awareness", "https://example.com/mental-health")

]

# Placeholder function ratings for demonstration
import random

formatted_output = []

for query, url in queries_urls:
    output_entry = {
        "Query": query,
        "URL": url,
        "Function Rating": random.randint(1, 5),  # Simulated rating
        "Custom Rating": random.randint(1, 5)  # Simulated rating
    }
    formatted_output.append(output_entry)

# Display the formatted output
formatted_output