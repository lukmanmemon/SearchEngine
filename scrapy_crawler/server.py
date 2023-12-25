from flask import Flask, request, render_template
import json
import search
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# TODO: (Optional tbh for the demo)
# On Server start, check to see whether the crawler/scraper has run and
# compiled its data, if not then do so ie. check for file Check to see if
# inverted indices have been generated from scraped data, if not do so


@app.route("/")
@cross_origin()
def display_spa():
    return render_template('index.html')


@app.route("/search")
@cross_origin()
def search_cosine_pagerank():
    query_string = request.args.get('query')
    search_results = search.search(query_string)
    return json.dumps(search_results)

if __name__ == "__main__":
    # we should uncomment the following for prod
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    app.run(port=3000, debug=True)
