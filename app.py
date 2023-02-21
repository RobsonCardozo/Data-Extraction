import os
import sys
from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient
import scrapy
import requests


app = Flask(__name__)

# paths
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'scripts'))


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org"]

    def parse(self, response):
        title = response.css("h1#firstHeading::text").get().strip()
        text = response.css("div#mw-content-text p::text").get().strip()
        
        yield {'title': title, 'text': text}

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
            'summary': text,
            'url': url
        }
        self.records.append(record)

    def __init__(self):
        super().__init__()
        self.records = []

    def closed(self, reason):
        if self.records:
            client = MongoClient('localhost', 27017)
            db = client['wikipedia']
            collection = db['baseconhecimento']
            collection.insert_many(self.records)


# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# home
@app.route('/')
def index():
    # MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['wikipedia']
    collection = db['baseconhecimento']

    # Spiderman, spiderman...
    spider = WikipediaSpider()
    spider.run()
    
    for record in spider.records:
        collection.update_one({'title': record['title']}, {'$set': record}, upsert=True)
    
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
