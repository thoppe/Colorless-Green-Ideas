Colorless Green Ideas
=====================

Generalizing Chomsky's [famous sentence](http://en.wikipedia.org/wiki/Colorless_green_ideas_sleep_furiously) into syntactic eigenvectors. 

### What does that mean? 

Consider Chomsky's sentence:

> Colorless green ideas sleep furiously.

The sentence is _gramatticly (syntax) correct_  but meaningless (semantics). 
It is hard to imagine an idea being both green and colorless and an idea that can sleep with fury.
It was posited as a sentence that had never been uttered before in the English lanuage, and without his thesis, probably never would be.
It is beautiful in its absurity, so let's create more!

### Noun phrases

Natural lanuage processing is hard, so let's restrict the problem to the titular project the `Colorless green idea`. This is a **noun phrase**, a particular one with the structure of `JJ JJ NN*` where `JJ` refers to an adjective and `NN*` refers to any noun variant (WordNet syntax).



# Getting Started:

To get started, build a noun phrase database. I built my from Wikipedia, and the tools for it can be found here [here](wiki_dump/).
If you'd rather not build your own, you can use the included database, [`JJ_noun_phrase.db`](`JJ_noun_phrase.db`), and simply run:

    python absurd_noun_pairs.py
