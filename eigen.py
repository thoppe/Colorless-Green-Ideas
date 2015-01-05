from __future__ import division
import sqlite3
import pandas as pd
import scipy.linalg

f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

noun_n = 50
adj_n  = noun_n*2

most_common_word = '''
SELECT {pos}.id, {pos}.name FROM {freq_name}
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
lookup_noun = dict(list(conn.execute(common_nouns)))
lookup_adj  = dict(list(conn.execute(common_adjs)))



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


df = pd.DataFrame(index=lookup_noun.values(),
                  columns=lookup_adj.values(),
                  dtype=float)

# Populate the dataframe
print "Populating dataframe"
for adj, noun, count in conn.execute(matching_adj_noun):
    df[adj][noun] = count

# Row normalize
print "Row normalizing"
def row_norm(row): return row/row.sum()
df = df.fillna(0).apply(row_norm, axis=1, raw=True)

print "Computing SVD"
U,s,V = scipy.linalg.svd(df)
print U
print U.shape

#import pylab as plt
#s /= s.max()
#plt.semilogy(s)
#plt.show()

exit()
