"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, json
from Homework_4 import app
import requests
import json
from IPython.display import HTML
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

subscription_key = "683934df678c4864b7d5f3ddbffffa3a"
assert subscription_key

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/searchPhoto', methods=['POST'])
def searchPhoto():
    search_term = request.form['searchTab']

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:15]]
    return json.dumps(thumbnail_urls)