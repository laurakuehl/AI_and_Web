from whoosh import index
from whoosh.qparser import QueryParser


# open Index
ix = index.open_dir("Task2/week2/indexdir") 

# Input for search
query_string = input("Enter search term: ")

# start search

with ix.searcher() as searcher:
    
    query = QueryParser("content", ix.schema).parse(query_string)
    results = searcher.search(query)

    # print all results
    for r in results:
        print(r)
        