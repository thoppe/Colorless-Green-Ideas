from __future__ import division
import random, itertools, sqlite3

f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

random_word_set_n = 20
matching_adj_noun_n = 20

most_common_noun = '''
SELECT nouns.name, nouns.id, count FROM freq_nouns
INNER JOIN nouns ON nouns.id=freq_nouns.id
ORDER BY freq_nouns.count DESC
LIMIT ?
'''

matching_adj_noun = '''
SELECT name, adj_noun_relation.count FROM adj_noun_relation
INNER JOIN adjs ON adjs.id=adj_noun_relation.adj_id
WHERE noun_id = ?
ORDER BY adj_noun_relation.count DESC LIMIT ?
'''

total_matching_adj_noun = '''
SELECT sum(adj_noun_relation.count) FROM adj_noun_relation
INNER JOIN adjs ON adjs.id=adj_noun_relation.adj_id
WHERE noun_id = ?'''

common_nouns = [item for item in 
                conn.execute(most_common_noun,(random_word_set_n,))]

def matching_words(noun_idx):
    vals = (noun_idx,matching_adj_noun_n)
    return list(conn.execute(matching_adj_noun,vals))


sele = random.choice(common_nouns)
noun, noun_idx, noun_freq = sele
total_count = conn.execute(total_matching_adj_noun, (noun_idx,)).next()[0]

print "** {} **".format(noun)

for adj, count in matching_words(noun_idx):
    percent = 100*count/total_count
    print " {:14s} {:14s}  ({:0.4f})".format(adj, noun, percent)

