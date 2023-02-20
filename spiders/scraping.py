import scrapy
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

class MercadoLivreSpider(scrapy.Spider):
    name = "mercado_livre"
    allowed_domains = ["mercadolivre.com.br"]
    start_urls = ["https://www.mercadolivre.com.br/"]

    def parse(self, response):
        preco = response.css(".price__fraction::text").get()
        produto = 'produto_teste'

        # Salva o resultado no banco de dados
        client = MongoClient('localhost', 27017)
        db = client['mercado_livre']
        collection = db['produtos']
        collection.insert_one({
            'produto': produto,
            'preco': preco
        })

def run_spider():
    process = CrawlerProcess()
    process.crawl(MercadoLivreSpider)
    process.start()

def get_results():
    client = MongoClient('localhost', 27017)
    db = client['mercado_livre']
    collection = db['produtos']
    results = []
    for item in collection.find().limit(10):
        results.append({
            'produto': item['produto'],
            'preco': item['preco']
        })
    return results
