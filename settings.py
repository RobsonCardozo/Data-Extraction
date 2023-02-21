BOT_NAME = 'wikipedia_spider'

SPIDER_MODULES = ['wikipedia_spider.spiders']
NEWSPIDER_MODULE = 'wikipedia_spider.spiders'

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
    'wikipedia_spider.pipelines.WikipediaSpiderPipeline': 300,
}
