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
common_nouns = 100
common_adjs  = 100
nouns = nouns.ix[common_nouns:,:eigenvalue_cut]
adjs  = adjs.ix[common_adjs:,:eigenvalue_cut]
var   = var[:eigenvalue_cut]
explained_variance = var.ix[:,0].sum()

# So we can multiply them together
var = var.as_matrix().reshape(-1)

print "Explained variance in sample: ", explained_variance

def anti_word(word,source,target,cutoff=-.002):
    # Returns an adjective that is far from the target

    distance = target.dot((source*var).T[word])
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

def quality_filter(noun, low=-0.075, high=-0.010):
    '''
    Generates absurd phrases that are not too absurd (which are boring,
    they use common adjectives), yet still have that je nes se pas
    '''
    total_score = 0
    while not low < total_score < high:
        phrase, scores = absurd_JJ_JJ_NN(noun, cutoff=cutoff)
        total_score = sum(scores)
    return phrase, scores
     
cutoff = -.005

for k in xrange(500):
    noun = np.random.choice(nouns.index)
    phrase, scores = quality_filter(noun)
    output = "{:.4f} {:20s}".format(sum(scores),' '.join(phrase))
    print output
