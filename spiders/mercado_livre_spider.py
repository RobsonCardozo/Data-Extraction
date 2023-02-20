from flask import Flask, render_template
import scrapy
from scrapy.crawler import CrawlerProcess

app = Flask(__name__)

@app.route("/")
def index():
    # Inicializa o scraper
    class MercadoLivreSpider(scrapy.Spider):
        name = "mercado_livre"
        allowed_domains = ["mercadolivre.com.br"]
        start_urls = ["https://www.mercadolivre.com.br/"]

        def parse(self, response):
            # Aqui você pode utilizar os seletores CSS ou XPATH para extrair os dados
            # do HTML da página.
            preco = response.css(".price__fraction::text").get()
            # Retorna o resultado para ser renderizado na página HTML
            yield {
                'produto': 'produto_teste',
                'preco': preco
            }

    # Roda o processo do Scrapy e guarda os resultados em uma lista
    process = CrawlerProcess()
    results = process.crawl(MercadoLivreSpider)
    results = results.get()

    return render_template("index.html", results=results)
