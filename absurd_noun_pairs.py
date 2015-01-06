from __future__ import division
import sqlite3
import pandas as pd

f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

nouns = pd.read_sql("SELECT * FROM PCA_nouns",conn,index_col="index")
adjs  = pd.read_sql("SELECT * FROM PCA_adjs", conn,index_col="index")

print len(nouns), len(adjs)
print "colorless" in adjs.index
a1= adjs.T["colorless"]
a2= adjs.T["green"]
a3= adjs.T["wooden"]
a4= adjs.T["red"]

#print a2
#exit()
print "Example output: "
print nouns.ix[:3,:4]
print adjs.ix[:3,:4]


query_word = "idea"
#noun = "design"
#noun = "original"
#adj1 = "
print "Reconstruction for {}".format(query_word)
n1 = nouns.T[query_word]

score = adjs.dot(n1)
score.sort(ascending=False,inplace=True)
print score



