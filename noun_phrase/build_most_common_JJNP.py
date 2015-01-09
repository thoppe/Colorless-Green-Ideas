import json, itertools
import sqlite3, codecs

f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

# Create indices and counting table
cmd_create_tables = '''
DROP TABLE IF EXISTS freq_nouns;
DROP TABLE IF EXISTS freq_adj;

CREATE TABLE IF NOT EXISTS freq_nouns (
    id INTEGER PRIMARY KEY,
    count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS freq_adj (
    id INTEGER PRIMARY KEY,
    count INTEGER NOT NULL
);
'''
conn.executescript(cmd_create_tables)

print "Counting the adjectives"
cmd_count_adj = '''
SELECT adjs.id, COUNT(*) FROM adj_noun_relation AS pair
INNER JOIN adjs ON adjs.id=pair.adj_id GROUP BY adjs.id'''
cmd_insert_into  = '''INSERT INTO {} {} {}'''
vals = "freq_adj","(id,count)",cmd_count_adj
conn.execute(cmd_insert_into.format(*vals))

print "Counting the nouns"
cmd_count_noun = '''
SELECT nouns.id, COUNT(*) FROM adj_noun_relation AS pair
INNER JOIN nouns ON nouns.id=pair.noun_id GROUP BY nouns.id'''
cmd_insert_into  = '''INSERT INTO {} {} {}'''
vals = "freq_nouns","(id,count)",cmd_count_noun
conn.execute(cmd_insert_into.format(*vals))

print "Building counting index"
cmd_count_idx = '''
CREATE INDEX IF NOT EXISTS idx_freq_adj ON freq_noun (count);
CREATE INDEX IF NOT EXISTS idx_freq_noun ON freq_adj (count);
'''

conn.commit()
