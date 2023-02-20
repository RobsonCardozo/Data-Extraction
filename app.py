from flask import Flask, render_template
from pymongo import MongoClient
from scripts.scraping import run_spider

app = Flask(__name__)

@app.route('/')
def index():
    client = MongoClient('localhost', 27017)
    db = client['wikipedia']
    collection = db['baseconhecimento']
    results = []
    for item in collection.find().limit(10):
        results.append({
            'title': item['title'],
            'summary': item['summary']
        })
    return render_template('index.html', results=results)

if __name__ == '__main__':
    # Rastreia a página da Wikipedia
    run_spider()

    app.run(debug=True)
