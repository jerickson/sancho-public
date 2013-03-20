sancho
=========

This is the code that runs sancho, the app I use to collect my favorite text from classic literature and track my reading lists.  The app lives at [jerickson.me](http://jerickson.me) if your intersted in seeing the simple UI i've built.  

###/books - core modules
  - **amazon.py** - Classes used for parsing Amazon kindle clippings files.
  - **api.py** - Public REST API.
  - **models.py** - The application data model.  Core application.
  - **google.py** - Simple interface I built to the Google Books API.  I use this API to help create books via ISBN13, view images for the book, and display a book summary on the book details page.

###/sanchoapp/static
  - **application.js** - Contains an experimental javascript class that I use to call the books API to define words a user highlights while reading Moby Dick on the site.  If you want to try it, go to [Moby Dick chapter 1](http://jerickson.me/book/moby-dick/text/chapter-1-loomings), and double click on a word to see it's definition.  Experimental only.
