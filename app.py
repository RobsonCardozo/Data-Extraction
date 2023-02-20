import sys
import os

from flask import Flask, render_template
from pymongo import MongoClient
from scripts.scraping import run_spider

app = Flask(__name__)

@app.route('/')
def index():
    client = MongoClient()
    db = client['mercado_livre']
    collection = db['produtos']
    results = []
    for item in collection.find().limit(10):
        results.append({
            'produto': item['produto'],
            'preco': item['preco']
        })
    return render_template('index.html', results=results)

client = MongoClient('localhost', 27017)
db = client['mercadolivre']
collection = db['produtos']

results = []
for item in collection.find():
    results.append({
        'produto': item['produto'],
        'preco': item['preco']
    })

if __name__ == '__main__':
    app.run(debug=True)
