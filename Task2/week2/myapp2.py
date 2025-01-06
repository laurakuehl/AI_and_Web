from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('start.html')

@app.route("/reversed")
def reversed():
    rev = request.args['rev'][::-1]
    return render_template('reversed.html', rev=rev)

@app.route("/search", methods=["GET"])
def search():
    query_string = request.args.get("query", "")
    results = []

    if query_string:
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(query_string)
            whoosh_results = searcher.search(query)

            results = [{"title": r["title"], "url": r.get("url", "#")} for r in whoosh_results]

    return render_template('search_results.html', query=query_string, results=results)
