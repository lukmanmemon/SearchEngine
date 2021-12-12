from flask import Flask, request
import json
import search

app = Flask(__name__)

# On Server start, check to see whether the crawler/scraper has run and compiled its data, if not then do so ie. check for file 
# Check to see if inverted indices have been generated from scraped data, if not do so




@app.route("/search")
def fbiOpenUpSearch():
    query_string = request.args.get('query')
    search_results = search.search(query_string)
    return json.dumps(search_results)

if __name__ == "__main__":
    # we should uncomment the following for prod
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    app.run(port=3000)
