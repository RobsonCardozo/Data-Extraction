BOT_NAME = 'wikipedia_scraper'

SPIDER_MODULES = ['wikipedia_scraper.spiders']
NEWSPIDER_MODULE = 'wikipedia_scraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "wikipedia_scraper.pipelines.WikipediaSpiderPipeline": 300,
}

MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DATABASE = "wikipedia_db"
MONGODB_COLLECTION = "wikipedia_pages"

DOWNLOAD_DELAY = 1
