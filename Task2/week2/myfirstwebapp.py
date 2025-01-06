from flask import Flask, request, render_template
from whoosh.index import open_dir

from textblob import TextBlob
from whoosh.query import Term
from pathlib import Path
from whoosh.qparser import MultifieldParser
from whoosh import scoring

app = Flask(__name__)

# Get the directory of week2
current_dir = Path(__file__).parent

# Construct the path to the index directory
index_dir = current_dir / "indexdir"
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

            search_results = searcher.search(q, terms=True)

            results = [
                {"title": r["title"], "url": r["url"],"snippet": r.get("snippet", "No snippet available."),"preview": r.highlights("content")}
                for r in search_results
            ]
            #if no result is found, use autocorrecter and search again for right spelling
            if not results:
                blob = TextBlob(q.text)
                corrected_query = blob.correct()
                print(f"No result for {q.text}, searching for {corrected_query}")
                search_results = searcher.search(Term("content", corrected_query.string))
                results = [
                    {"title": r["title"], "url": r["url"]}
                    for r in search_results
                ]
    return render_template("search.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)