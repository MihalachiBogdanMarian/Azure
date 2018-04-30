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
import pyodbc

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

@app.route("/getProp/<url>", methods=["POST"])
def getProp(url):
	subscription_key = "f3b511f4df724117af62d1fb82041eda"
	assert subscription_key
	vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
	vision_analyze_url = vision_base_url + "analyze"
	url = "https://" + url
	headers = {'Ocp-Apim-Subscription-Key': subscription_key }
	params = {'visualFeatures': 'Categories,Description,Color'}
	data = {'url': url}
	response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
	response.raise_for_status()
	analysis = response.json()
	image_caption = analysis["description"]["captions"][0]["text"].capitalize()
	return json.dumps(image_caption)

@app.route("/addInBd/<url>/<description>", methods=["POST"])
def addInBd(url, description):
    url = "https://" + url
    server = 'azurebidi.database.windows.net'
    database = 'ImagesTornado'
    username = 'AzureBidi'
    password = 'Azure6598'
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Image (ImageLink, ImageDescription) VALUES('" + url + "', '" + description.split("\"")[1] + "')")
    cnxn.commit()
    cnxn.close()
    return json.dumps("OK")