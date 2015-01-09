import json, itertools
import sqlite3, codecs
from copy import deepcopy
from bs4 import BeautifulSoup
import bs4

f_db  = "wiki.db"
extract_directory = "extract"

conn = sqlite3.connect(f_db, check_same_thread=False)
cmd_create_table = '''
CREATE TABLE IF NOT EXISTS wiki(
  wikipedia_id INTEGER PRIMARY KEY,
  title STRING,
  text  STRING,
  length INT
);'''

cmd_add = '''
INSERT OR IGNORE INTO wiki 
(wikipedia_id, title, text, length)
VALUES
(?,?,?,?)
'''

conn.execute(cmd_create_table)
conn.commit()


import fnmatch
import os

print "Finding filenames"
F_WIKI = []
for root, dirnames, filenames in os.walk(extract_directory):
  for filename in fnmatch.filter(filenames, 'wiki_*'):
      F_WIKI.append(os.path.join(root, filename))

#F_WIKI = ["tmp",]


def unpack_data(data):
    keys = "wikipedia_id", "title", "text", "length"
    return tuple(data[k] for k in keys)

_trucate_sections = set(["see also",
                         "references",
                         "further reading",
                         "external links"])

def is_truncate_section(section_text):
  if section_text==None:
    return False
  return section_text.strip().lower() in _trucate_sections 

def strip_extra(soup):
    # Remove all items that are not "content"
    remove_list = []
    for x in soup.findAll("h2", text=is_truncate_section):
      for y in x.next_siblings:
        remove_list.append(y)
      remove_list.append(x)
      break

    for item in remove_list:
      item.extract()

    return soup

def doc_iter(f_wiki):
  with codecs.open(f_wiki,'r','utf-8') as FIN:
    block = []
    for line in FIN:
      if line.lstrip()[:4]==u"<doc":
        if block: 
          yield ' '.join(block)
          block = []
      block.append(line)

def parse_wiki(f_wiki):

    insert_data = []
    for raw_doc in doc_iter(f_wiki):
      doc = BeautifulSoup(raw_doc,'lxml').doc
      doc = strip_extra(doc)     
      text = unicode(doc)

      data = {"wikipedia_id":int(doc["id"]),
              "title":unicode(doc["title"]),
              "text":text,
              "length":len(text)}

      insert_data.append(unpack_data(data))

    print "Returned {} titles from {}".format(len(insert_data),f_wiki)
    return tuple(insert_data)


F_WIKI = sorted(F_WIKI)
#F_WIKI = ["tmp"]

import multiprocessing as mp
P = mp.Pool(30)
for data_block in P.imap(parse_wiki, F_WIKI):
#for data_block in itertools.imap(parse_wiki, F_WIKI):
  #print len(data_block)
  conn.executemany(cmd_add, data_block)
conn.commit()



