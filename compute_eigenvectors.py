from __future__ import division
import sqlite3
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

noun_n = 2000
adj_n  = 10000
variance_ratio = 0.50

query_word = "cat"

most_common_word = '''
SELECT {pos}.name FROM {freq_name}
INNER JOIN {pos} ON {pos}.id={freq_name}.id
ORDER BY {freq_name}.count DESC
LIMIT {limit}
'''
common_nouns = most_common_word.format(pos="nouns",
                                       freq_name="freq_nouns",
                                       limit=noun_n)
common_adjs  = most_common_word.format(pos="adjs",
                                       freq_name="freq_adj",
                                       limit=adj_n)
nouns = list([x[0] for x in conn.execute(common_nouns)])
adjs  = list([x[0] for x in conn.execute(common_adjs)])

assert(query_word in nouns)

cmd_common_noun_id = '''
SELECT nouns.id FROM freq_nouns
INNER JOIN nouns ON nouns.id=freq_nouns.id
ORDER BY freq_nouns.count DESC
LIMIT {limit}
'''.format(limit=noun_n)

cmd_common_adj_id = '''
SELECT adjs.id FROM freq_adj
INNER JOIN adjs ON adjs.id=freq_adj.id
ORDER BY freq_adj.count DESC
LIMIT {limit}
'''.format(limit=adj_n)

matching_adj_noun = '''
SELECT adjs.name, nouns.name, count FROM adj_noun_relation AS rel
INNER JOIN adjs  ON adjs.id =rel.adj_id
INNER JOIN nouns ON nouns.id=rel.noun_id
WHERE rel.noun_id IN ({})
AND   rel.adj_id  IN ({})
'''.format(cmd_common_noun_id, cmd_common_adj_id)


df = pd.DataFrame(index=nouns,
                  columns=adjs,
                  dtype=float)

# Populate the dataframe
print "Populating dataframe"
for adj, noun, count in conn.execute(matching_adj_noun):
    df[adj][noun] = count

# Row normalize
print "Row normalizing"
def row_norm(row): return row/row.sum()
df = df.fillna(0).apply(row_norm, axis=1, raw=True)

#print "Computing SVD"
print "Computing PCA"
pca = PCA(n_components=variance_ratio)
U = pca.fit_transform(df)
pca_score = pca.explained_variance_ratio_
V = pca.components_
msg = "PCA required {} components for an explained variance of {}"
print msg.format(pca.n_components, pca_score.sum())

nouns_pca = pd.DataFrame(U, index=nouns)
adjs_pca  = pd.DataFrame(V.T, index=adjs)

print "Example output: "
print nouns_pca.ix[:3,:4]
print adjs_pca.ix[:3,:4]

#noun = "design"
#noun = "original"
#adj1 = "
print "Reconstruction for {}".format(query_word)
n1 = nouns_pca.T[query_word]
score = adjs_pca.dot(n1)
score.sort(ascending=False,inplace=True)
print score



