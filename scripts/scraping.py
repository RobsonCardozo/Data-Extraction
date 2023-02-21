import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Main_Page"]

    def parse(self, response):
        # Extrai o título da página
        title = response.css('title::text').get()

        # Extrai o resumo da página
        summary = response.css('meta[name="description"]::attr(content)').get()

        # Consulta a API da Wikipedia para obter informações adicionais sobre o título
        api_url = "https://en.wikipedia.org/w/api.php"
        api_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "titles": title,
            "exsentences": 2,
            "explaintext": True,
            "inprop": "url"
        }
        api_response = requests.get(api_url, params=api_params).json()

        # Extrai informações adicionais do resultado da API
        page = next(iter(api_response["query"]["pages"].values()))
        full_summary = page["extract"]
        url = page["fullurl"]

        # Salva o resultado no banco de dados
        client = MongoClient('localhost', 27017)
        db = client['wikipedia']
        collection = db['baseconhecimento']
        collection.insert_one({
            'title': title,
            'summary': summary,
            'full_summary': full_summary,
            'url': url
        })

def run_spider():
    process = CrawlerProcess()
    process.crawl(WikipediaSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
