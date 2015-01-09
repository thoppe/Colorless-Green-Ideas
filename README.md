Colorless Green Ideas
=====================

Generalizing Chomsky's [famous sentence](http://en.wikipedia.org/wiki/Colorless_green_ideas_sleep_furiously) into syntactic singular vectors. 

### What does that mean? 

Consider Chomsky's sentence:

> Colorless green ideas sleep furiously.

The sentence is _gramatticly correct_ (syntax) but _meaningless_ (semantics). 
It is hard to imagine an idea being both green and colorless and that an idea that can sleep with fury.
It was posited as a sentence that had never been uttered before in the English lanuage, and without his thesis, probably never would be.
It is beautiful in its absurity, so let's create more!

### Noun phrases

Natural lanuage processing is hard, so let's restrict the problem to the titular project, the `Colorless green idea`. 
This is a **noun phrase**, a particular one with the structure of `JJ JJ NN*` where `JJ` refers to an adjective and `NN*` refers to any noun variant (WordNet syntax).
If we had some large corpus of text we could find all noun phrases of the type `JJ ... JJ NN*` and assoicate each adjective with the cooresponding noun, essentially a bigram database.

### Syntactic singular vectors

If the goal is to create meaningless noun phrases, a bigram database won't give us anything that we haven't seen before.
This is unacceptable.
Therefore, we seek a decompostion and perform a singular value decomposition over the (noun) normalized database.
We specificly keep the explained variance moderate, if it was too high it would simply recreate the bigram database, if it was too low we would low word relations.
This naturally fuzzes the data; the left singular vectors represent a subspace where nouns are correlated to other nouns that share common adjectives and the right singular vectors represent a subspace where the adjectives are correlated to other adjectives that share a common noun.
Simple right?

### `JJ JJ NN`

Starting with a noun `NN`, we choose a set of adjectives that are ["far away"](http://mathworld.wolfram.com/L2-Norm.html) from that noun. 
Selecting the first one `JJ1`, we select a second adjective `JJ2` that far away from the first adjective `JJ1`.
This gives us a score for each of the pairings, `JJ1,JJ2`, `JJ1,NN`, `JJ2,NN`. 
Using the sample database, a human arbiturary decided that a combined score s, in the range of `-0.075 < s < -0.010` was optimal.
Why have a lower bound?
It turns out that phrases that have very absurd scores are simply common words that are othorognal to each other like places and colors, the correct output but boring. 
I prefer a "industrial legislative falcon".

### Examples

Here are some of my favorites:

````
-0.0290 severe municipal jazz
-0.0329 old sole beard      
-0.0371 hot racial archbishop
-0.0428 municipal professional everything
-0.0427 legal high ballad   
-0.0427 single spanish sin  
-0.0420 successful specific seal
-0.0419 chief live foliage  
-0.0417 spiritual guilty warship
-0.0393 agricultural professional click
-0.0382 possible urban king 
-0.0381 coastal senior methodology
-0.0365 entire dry institutes
-0.0328 federal minor upbringing
-0.0308 secret psychological fragment
-0.0305 professional free gown
-0.0297 earliest electric litigation
````

## Getting Started:

To get started, build a noun phrase database. 
I built my from Wikipedia, and the tools for it can be found in this repository [here](wiki_dump/).
If you'd rather not build your own, you can use the included database, `JJ_noun_phrase.db` and simply run:

    python absurd_noun_pairs.py

## Requires

[Alot](http://hyperboleandahalf.blogspot.com/2010/04/alot-is-better-than-you-at-everything.html) of modules ... `pandas`, `sqlite`, `numpy`, `sklearn`, `BeautifulSoup`, `nltk`, `pattern.en`.