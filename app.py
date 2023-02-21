import os
import sys
import requests
from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from pymongo import MongoClient
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Main_Page"]

    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.records = []

    def parse(self, response):
        title = response.css("h1#firstHeading::text").get().strip()
        summary = response.css("div#mw-content-text p::text").get().strip()

        # Consulta a API da Wikipedia para obter informações adicionais sobre o título
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "prop": "extracts|info",
                "titles": title,
                "exsentences": 2,
                "explaintext": True,
                "inprop": "url"
            }
        ).json()

        page = next(iter(response["query"]["pages"].values()))
        url = page["fullurl"]

        record = {
            'title': title,
            'summary': summary,
            'url': url,
            'query': self.query
        }
        self.records.append(record)

    def closed(self, reason):
        if self.records:
            collection.insert_many(self.records)  # insert any remaining records
        self.client.close()  # close the MongoDB client connection

app = Flask(__name__)

# MongoDB connection
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'wikipedia'
MONGO_COLLECTION = 'baseconhecimento'

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

# Flask app routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    results = []
    for item in collection.find():
        results.append({
            'title': item['title'],
            'summary': item['summary'],
            'url': item['url']
        })
    return render_template('index.html', results=results)

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))

    spider = WikipediaSpider(query=query)
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()

    # Retrieve the search results from MongoDB
    results = collection.find({'query': query})

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
