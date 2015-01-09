# -*- coding: utf-8 -*-
import itertools, string
import sqlite3, codecs


f_db = "JJ_noun_phrase.db"
f_NP = "gen/raw_NP.txt"

conn = sqlite3.connect(f_db)

cmd_drop_raw_table = '''
DROP TABLE IF EXISTS raw_JJNP;
DROP INDEX IF EXISTS idx_raw_noun;
DROP INDEX IF EXISTS idx_raw_adj;
DROP INDEX IF EXISTS idx_raw_pairs;
'''

cmd_create_inital_tables = '''
CREATE TABLE raw_JJNP (
  adj  STRING,
  noun STRING
);'''
cmd_add_raw = "INSERT INTO raw_JJNP (adj,noun) VALUES (?,?)"
cmd_raw_index = '''
CREATE INDEX IF NOT EXISTS idx_raw_noun ON raw_JJNP(noun);
CREATE INDEX IF NOT EXISTS idx_raw_adj ON raw_JJNP(adj); 
CREATE INDEX IF NOT EXISTS idx_raw_pairs ON raw_JJNP(adj,noun);
'''

def replace_em_dash(word):
    return word.replace(u'–',u'-')

letter_set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-")
def is_extended_alpha(word):
    letters = set(word)
    return letter_set.issuperset(letters)

def pattern_iter(line):
    words = line.split('JJ')[0].strip().split()

    if words:
        noun = words[-1]
        for adj in words[:-1]:
            yield replace_em_dash(adj), replace_em_dash(noun)

def raw_iter(f_NP):
    with codecs.open(f_NP, 'r','utf-8') as FIN:
        for k,line in enumerate(FIN):
            if k and k%100000==0: 
                print u"Raw insert of {}/{}".format(k,line.strip())
            for adj,noun in pattern_iter(line):                
                if (len(adj)>2 and len(noun)>2 and 
                    is_extended_alpha(adj) and 
                    is_extended_alpha(noun)):
                    yield adj, noun

# Raw insert
conn.executescript(cmd_drop_raw_table)
conn.executescript(cmd_create_inital_tables)
conn.executemany(cmd_add_raw, raw_iter(f_NP))

print "Building indices"
conn.executescript(cmd_raw_index)

cmd_create_tables = '''
DROP TABLE IF EXISTS nouns;
DROP TABLE IF EXISTS adjs;
DROP TABLE IF EXISTS adj_noun_relation;

CREATE TABLE IF NOT EXISTS nouns(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name STRING UNIQUE
);

CREATE TABLE IF NOT EXISTS adjs(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name STRING UNIQUE
);

-- Semantic relation between adjective and noun
CREATE TABLE IF NOT EXISTS adj_noun_relation(
  adj_id INTEGER NOT NULL,
  noun_id INTEGER NOT NULL,
  count INTEGER NOT NULL,
  UNIQUE (adj_id, noun_id)
);
'''
conn.executescript(cmd_create_tables)

cmd_select_nouns = '''SELECT noun FROM raw_JJNP GROUP BY noun '''
cmd_select_adjs  = '''SELECT adj  FROM raw_JJNP GROUP BY adj  '''
cmd_insert_into  = '''INSERT INTO {} {} {}'''

print "Inserting singletons"
conn.execute(cmd_insert_into.format("nouns", "(name)", cmd_select_nouns))
conn.execute(cmd_insert_into.format("adjs" , "(name)", cmd_select_adjs))

print "Inserting pairs"
cmd_select_pairs = '''
SELECT 
--raw.adj,raw.noun,
adjs.id,nouns.id,COUNT(*) FROM raw_JJNP AS raw
INNER JOIN nouns ON raw.noun=nouns.name
INNER JOIN adjs  ON raw.adj =adjs.name
GROUP BY raw.adj,raw.noun'''
conn.execute(cmd_insert_into.format("adj_noun_relation", 
                                    "(adj_id,noun_id,count)",
                                    cmd_select_pairs))


print "Dropping raw table"
conn.executescript(cmd_drop_raw_table)

print "Building pair index"
cmd_create_pair_index = '''
CREATE INDEX IF NOT EXISTS idx_adj_id ON adj_noun_relation (adj_id);
CREATE INDEX IF NOT EXISTS idx_noun_id ON adj_noun_relation (noun_id);
'''
conn.executescript(cmd_create_pair_index)

conn.commit()
