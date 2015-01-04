### Tools to extract the needed information from wikipedia.

## Building `wiki.db`

1. Download the file [`enwiki-latest-pages-articles.xml`](https://dumps.wikimedia.org/enwiki/latest/).
2. Run `WikiExtractor.py` to expand out the xml into easily parsable blocks.
3. Run `build_database.py` to build the inital wiki database.

## Building `JJ_noun_phrase.db`

1. Run `noun_phrase_extract.py` to extract all the noun phrases into raw text.
2. Run `build_NP_JJ_database.py` to pull those phrases into a database.
3. Run `build_most_common_JJNP.py` to compute statistics and indices.






