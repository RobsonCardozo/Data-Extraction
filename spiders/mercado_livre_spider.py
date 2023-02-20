import scrapy


class MercadoLivreSpider(scrapy.Spider):
    name = "mercado_livre"
    allowed_domains = ["mercadolivre.com.br"]
    start_urls = ["https://www.mercadolivre.com.br/"]

    def parse(self, response):
        # Aqui você pode utilizar os seletores CSS ou XPATH para extrair os dados
        # do HTML da página.
        preco = response.css(".price__fraction::text").get()
        pass
