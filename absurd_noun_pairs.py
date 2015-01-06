from __future__ import division
import sqlite3
import pandas as pd
import numpy as np

f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

nouns = pd.read_sql("SELECT * FROM PCA_nouns",conn,index_col="index")
adjs  = pd.read_sql("SELECT * FROM PCA_adjs", conn,index_col="index")
var   = pd.read_sql("SELECT * FROM PCA_explained_variance", conn,index_col="index")

eigenvalue_cut = 300
nouns = nouns.ix[:,:eigenvalue_cut]
adjs  = adjs.ix[:,:eigenvalue_cut]
var   = var.ix[:eigenvalue_cut]
explained_variance = var.ix[:,0].sum()
print "Explained variance in sample: ", explained_variance

def anti_word(word,source,target,cutoff=-.002):
    # Returns an adjective that is far from the target

    distance = target.dot(source.T[word])
    distance.sort()
    distance /= np.linalg.norm(distance)
    distance = distance[(distance < cutoff)]
    idx = np.random.randint(len(distance))
    return distance, distance[idx], distance.index[idx]

def absurd_JJ_JJ_NN(noun=None, cutoff=-0.002):
    if noun == None:
        noun = np.random.choice(nouns.index)
        
    distance1, s1, a1 = anti_word(noun, nouns, adjs, cutoff)

    wx = adjs.T[distance1.index]
    while True:
        try:
            distance2, s2, a2 = anti_word(a1, wx.T, wx.T, cutoff)
            break
        except:
            cutoff /= 2

    scores = s2, distance1[a1], distance2[a2]
    return (a1,a2,noun), scores

cutoff = -.005

noun = "idea"

for k in xrange(2000):
    phrase, scores = absurd_JJ_JJ_NN(noun="idea", cutoff=cutoff)
    #print len(distance1), len(distance2)
    #print "({}) {} {}".format(*scores)
    print ' '.join(phrase), sum(scores)
