import os
import sys
from distutils import debug
from scripts.scraping import run_spider
from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['wikipedia']
    collection = db['baseconhecimento']
    results = []
    for item in collection.find():
        results.append({
            'title': item['title'],
            'summary': item['summary'],
            'url': item['url']
        })
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
    run_spider()
