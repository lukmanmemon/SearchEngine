from flask import Flask
import json
import search

app = Flask(__name__)


@app.route("/")
def fbiOpenUpSearch():
    # FOr now this is just the default search, will include the route/query params on next commit
    search_results = search.search("students in Ryerson University and York University")
    print(search_results)
    return json.dumps(search_results)

if __name__ == "__main__":
    # we should uncomment the following for prod
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    app.run(port=3000)
