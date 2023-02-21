import json
from pymongo import MongoClient

class WikipediaSpiderPipeline:
    def open_spider(self, spider):
        self.records = []

    def close_spider(self, spider):
        if self.records:
            # Connect to MongoDB database and insert records
            client = MongoClient("<your-mongodb-connection-string>")
            db = client["<your-mongodb-database>"]
            collection = db["<your-mongodb-collection>"]
            collection.insert_many(self.records)

    def process_item(self, item, spider):
        self.records.append(dict(item))
        return item
