## Tools to build a noun phrase database from wikipedia.

A bit of warning, Wikipeida is **big** and SVD isn't cheap. 
Don't worry, you'll figure it out.

### Building `wiki.db`

1. Download the file [`enwiki-latest-pages-articles.xml`](https://dumps.wikimedia.org/enwiki/latest/).
2. Run [`WikiExtractor.py`](WikiExtractor.py) to expand out the xml into easily parsable blocks. To run it with 2.5 MB chunks:
````
cat enwiki-latest-pages-articles.xml | python WikiExtractor.py  -o extract/ -b 2500K -s
````
3. Run [`build_database.py`](build_database.py) to build the inital wiki database.

### Building `JJ_noun_phrase.db`

1. Run [`noun_phrase_extract.py`](noun_phrase_extract.py) to extract all the noun phrases into raw text.
2. Run [`build_NP_JJ_database.py`](build_NP_JJ_database.py) to pull those phrases into a database.
3. Run [`build_most_common_JJNP.py`](build_most_common_JJNP.py) to compute statistics and indices.
4. Run [`compute_eigenvectors.py`](compute_eigenvectors.py) to perform the singular value decomposition.






