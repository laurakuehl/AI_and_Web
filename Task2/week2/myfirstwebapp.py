from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from textblob import TextBlob
from whoosh.query import Term

app = Flask(__name__)

# Open Whoosh index
index_dir = "indexdir"
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