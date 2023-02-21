import scrapy
import requests
from pymongo import MongoClient


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
            'summary': summary,
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

def run_spider():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(WikipediaSpider)
    process.start()
