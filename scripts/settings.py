ITEM_PIPELINES = {
    'scraping.pipelines.MongoDBPipeline': 300,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "wikipedia"
MONGODB_COLLECTION = "baseconhecimento"
