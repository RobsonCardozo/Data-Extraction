import pymongo

class WikipediaSpiderPipeline:
    collection_name = 'wikipedia_pages'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def process_item(self, item, spider):
        with pymongo.MongoClient(self.mongo_uri) as client:
            db = client[self.mongo_db]
            db[self.collection_name].insert_one(dict(item))
        return item

__all__ = ["WikipediaSpiderPipeline"]
