# Task 2
`Task2` is separated into two sections: `week1` and `week2`. The final implementation of task 2, and all that is required to run the webapp, can be found in `week2`. 

The task was to create and deploy a simple search engine that searches the contents of one website and its subsites for search terms that the user inputs.

## The Crawler
In `crwl.py` you will find the crawler that crawls the https://www.uni-osnabrueck.de/ website.

- The schema consists of:
  - `title`: stores the title of the web page
  - `content`: stores the main text of the web page
  - `url`: stores the URL of the web page
  - `snippet`: stores a short preview or snippet of the content
    - The snippet was created to store the first 150 characters of the content text to use it as the preview for the results in the `search.html`. This is now deprecated because of Whoosh's `.preview` function.
      
The crawling loop visits all URLs on the `agenda` and saves the required contents and URL in the `whoosh index`. This index is saved in `indexdir/`. 
Important to note: The crawler does not crawl any websites that do not use the prefix 'https://www.uni-osnabrueck.de/'. 

The crawler can be run when executing the `crwl.py` and runs independently of `myfirstwebapp.py`. 

## The Webapp
With `myfirstwebapp.py`, a Flask app can be run that utilizes the before created index, the .html files in `templates/` and a search structure. 

- The `home` function and `home.html`:
  - displays the title of the search engine
  - contains a form action that lets the user submit a search term
- The `search` function:
  - gets the user input and uses it as the query for the search
  - weighs the title twice as much as the content text when establishing an order for showing the results
  - highlights the search term in the preview texts of the results
  - saves results in the `results` dictionary
  - uses Whoosh's auto correction to search again for the corrected spelling of the term if no results were found
  - renders the `search.html` and passes the query and results
- The `search.html`:
  - displays the results of the search with the titel of the web page and the preview text with the highlightet query
  - has a 'Back to Home' button to navigate to the `home` function again for a new search

## Server Deployment
The `myfirstreverse.wsgi` imports the flask app from `myfirstwebapp.py` as the application.
The `requirements.txt` is used to install all dependencies of the webapp.

These files and folders are used to deploy our webapp on the uni server:
- indexdir/
- templates/
- myfirstreverse.wsgi
- myfirstwebapp.py
- requirements.txt

You can access our webapp, when connected to the university network, [here](http://vm146.rz.uni-osnabrueck.de/u044/myfirstreverse.wsgi/).
