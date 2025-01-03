from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)

# Open Whoosh index
index_dir = "Task2/week2/indexdir"
ix = open_dir(index_dir)

@app.route("/")
def home():
    """Display search form."""
    return render_template("home.html")

@app.route("/search")
def search():
    """Perform a search and display results."""
    query = request.args.get("q", "")
    results = []

    if query:
        with ix.searcher() as searcher:
            qp = QueryParser("content", ix.schema)
            q = qp.parse(query)
            search_results = searcher.search(q)
            results = [
                {"title": r["title"], "url": r["url"]}
                for r in search_results
            ]

    return render_template("search.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)