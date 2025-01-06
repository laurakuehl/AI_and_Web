import requests
from bs4 import BeautifulSoup
from pathlib import Path
from whoosh.index import create_in, open_dir
from whoosh.writing import AsyncWriter
from whoosh.fields import Schema, TEXT, ID
import os

# Prefix und Start-URL
prefix = 'https://vm009.rz.uos.de/crawl/'

#start_url = prefix+'home.html'
start_url = prefix + 'index.html'

# Get the directory of week2
current_dir = Path(__file__).parent

# Construct the path to the index directory
index_dir = current_dir / "indexdir"


# Schema definieren
schema = Schema(
    title=TEXT(stored=True),  # Titel speichern
    content=TEXT(stored=True),  # Content speichern
    url=ID(stored=True),  # URL speichern
    snippet=TEXT(stored=True)
)

if not os.path.exists(index_dir):
    os.mkdir(index_dir)

try:
    ix = open_dir(index_dir)  # try to oopen the index
except:
    ix = create_in(index_dir, schema)  # create index if not existed

agenda = [start_url]

visited = set()
stored_urls = []
while agenda:
    url = agenda.pop() # next URL from the agenda
    
    #check whether URL is already represented in index to avoid doubles when crawler runs multiple times 
    with ix.searcher() as searcher:
        for docnum, fields in enumerate(searcher.all_stored_fields()):
            stored_urls.append(fields.get('url', 'No URL'))            
    if url in stored_urls: 
        continue  

    print("Get ",url)
    try:
        r = requests.get(url, timeout=5)  # HTTP-inquiry
        print(r, r.encoding)
        if r.status_code != 200:
            continue
    except requests.RequestException as e:
        print("Fehler beim Abrufen von {}: {}".format(url, e))
        continue

    visited.add(url)  # mark URL

    # HTML-input parse
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.title.string if soup.title else "No Title"

    
    # remove problematic tags
    for script_or_style in soup.find_all(['script', 'style', 'noscript', 'header']):
        script_or_style.decompose()  # remove the tags

    # extract only text
    content = soup.get_text(separator=" ", strip=True)  # separator=" check if the text is good seperated
    content = content[:1000]  # only the first 1000 elements

    # Create a snippet (first 150 characters or a meaningful preview)
    snippet = content[:150] + "..." if len(content) > 150 else content

    # debugging
    print(f"Content length: {len(content)}")
    print(f"Content preview: {content[:200]}...")

    # check if only strings are saved
    if not isinstance(content, str):
        print(f"Content is not a string for {url}: {type(content)}")
        continue

     # safe in woosh index
    writer = AsyncWriter(ix)
    try:
        writer.add_document(title=title, content=content, url=url, snippet=snippet)
        writer.commit()
        print(f"Dokument gespeichert: {title} ({url})")
    except Exception as e:
        print(f"Fehler beim Speichern von {url}: {e}")

    # extract all links and add them to the agenda
    for link in soup.find_all('a', href=True):
        full_url = requests.compat.urljoin(prefix, link['href'])
        if full_url.startswith(prefix) and full_url not in visited:
            agenda.append(full_url)

        