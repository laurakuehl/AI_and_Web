from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh import scoring

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
        with ix.searcher(weighting=scoring.BM25F()) as searcher:

            # weights for fields: title is twice as important as content
            field_weights = {"title": 2.0, "content": 1.0}
            
            # MultifieldParser for querying multiple fields
            qp = MultifieldParser(["title", "content"], ix.schema, fieldboosts=field_weights)
            q = qp.parse(query)

            search_results = searcher.search(q)
            results = [
                {"title": r["title"], "url": r["url"]}
                for r in search_results
            ]

    return render_template("search.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)