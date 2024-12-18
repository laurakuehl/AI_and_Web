from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)

# Open Whoosh index
index_dir = "indexdir"
ix = open_dir(index_dir)

@app.route("/")
def home():
    """Display search form."""
    return """
        <form action="/search" method="get">
            <input type="text" name="q" placeholder="Search for...">
            <button type="submit">Search</button>
        </form>
    """

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