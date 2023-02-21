import os
import json
import requests

from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
import scrapy


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Main_Page"]

    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.records = []

    def parse(self, response):
        title = response.css("h1#firstHeading::text").get().strip()
        summary = response.css("div#mw-content-text p::text").get().strip()

        # Query Wikipedia API for additional information about the title
        api_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "titles": title,
            "exsentences": 2,
            "explaintext": True,
            "inprop": "url",
        }
        api_response = requests.get(api_url, params=params).json()

        page = next(iter(api_response["query"]["pages"].values()))
        url = page["fullurl"]

        record = {"title": title, "summary": summary, "url": url, "query": self.query}
        self.records.append(record)

    def closed(self, reason):
        # Save results to a JSON file
        file_path = os.path.join(os.getcwd(), "data", f"{self.query}.json")
        with open(file_path, "w") as f:
            json.dump(self.records, f)


app = Flask(__name__)

# Flask app routes
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return redirect(url_for("index"))

    # Run the spider to fetch data
    spider = WikipediaSpider(query=query)
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()

    # Redirect to the results page
    return redirect(url_for("show_results", query=query))

@app.route("/results/<query>")
def show_results(query):
    # Load results from the JSON file
    file_path = os.path.join(os.getcwd(), "data", f"{query}.json")
    with open(file_path, "r") as f:
        records = json.load(f)

    return render_template("results.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
