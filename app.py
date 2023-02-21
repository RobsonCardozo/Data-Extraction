import os
import sys
from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient
from scripts.scraping import run_spider

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['wikipedia']
    collection = db['baseconhecimento']

    if collection.count_documents({}) == 0:
        collection.insert_one({
            'title': '',
            'summary': '',
            'url': ''
        })

    results = []
    for item in collection.find():
        results.append({
            'title': item['title'],
            'summary': item['summary'],
            'url': item['url']
        })
    return render_template('index.html', results=results)

if __name__ == '__main__':
    run_spider()
    app.run(debug=True)
