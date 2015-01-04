import itertools, collections
import sqlite3
import bs4
import nltk
from pattern.en import singularize, lemma, parsetree

f_db  = "wiki.db"
conn = sqlite3.connect(f_db, check_same_thread=False)

#print "Creating index"
cmd_index = '''CREATE INDEX IF NOT EXISTS 
idx_title ON wiki(title)'''
conn.execute(cmd_index)
conn.commit()

# Split into sections (based of h2 tags)
def section_iterator(soup):
    for x in soup.findAll("h2"):
        text  = unicode(x.next_sibling).strip()
        title = unicode(x.text).strip()
        loc = text.find(u"{}.".format(title))
        if loc==0:
            text = text[len(title)+1:].lstrip()
        yield title, text

def compute_sentences(text):

    # Remove everything past the "references" section
    ref_token = u"== References =="
    if ref_token in text:
        text = text.split(ref_token)[0]

    # First tokenize the wiki content into paragraphs by newlines
    paragraphs = [line.strip() for line in text.split('\n') if line]

    # Find the paragraphs the are headers, denoted by === and remove them
    text_blocks = collections.defaultdict(list)
    for para in paragraphs:
        if para[:2] == "==" and para[-2:] == "==":
            text_blocks["header"].append(para)
        else:
            text_blocks["content"].append(para)

    text = ' '.join(text_blocks["content"])

    # Tokenize by sentences
    sentences = nltk.tokenize.sent_tokenize(text)

    # Filter for short sentences (<= 3 words) or those not ending in punctuation
    ending_tokens = '''.?!;:")'''
    def is_sentence(s):
        if len(s.split()) <= 3: return False   
        if s[-1] not in ending_tokens:
            return False
        return True

    return filter(is_sentence, sentences)

def find_noun_phrases(sentence):
    # Find all noun phrases with at least two words that have sementatic meaning
    T = parsetree(sentence, relations=True, lemmata=True)
    items = []
    for sentence in T:
        for chunk in sentence.chunks:
            if chunk.type == "NP":
                phrase = []
                for word in chunk.words:
                    if (word.type[0:2] in ["JJ","NN","RB","VB"] and 
                        len(str(word))>2):
                        phrase.append((word.lemma,word.type))
                if len(phrase) > 1:
                    items.append(phrase)
    return items


def compute_NP(text):
    sentences = compute_sentences(text)
    
    for s in sentences:
        meaningful_noun_phrases = [x for x in find_noun_phrases(s) 
                                   if len(x)>1]
        for phrase in meaningful_noun_phrases:
            words, pos = zip(*phrase)
            words, pos = u' '.join(words), u' '.join(pos)
            words = words.replace('.','').replace('!','').replace('?','')
            yield words, pos


def noun_phrase_from_text(text):
    html = u"<html>{}</html>".format(text)
    #if type(text)==tuple: text = text[0]
    soup = bs4.BeautifulSoup(html)

    # Remove all list items
    li_items = list(soup.findAll("li"))
    bad_li = [x for x in soup.findAll("li")]
    for x in bad_li:
        x.decompose()

    for section_name,text in section_iterator(soup):
        for phrase, pos in compute_NP(text):
            yield phrase, pos

def descriptive_noun_phrase(pos):
    # Keep only those NP that are JJ .. JJ, (NN|NNS)
    for p in pos.split()[:-1]:
        if p != "JJ": return False
    return True

def phrase_block(text):
    r_val = []
    for phrase, pos in noun_phrase_from_text(text):
        if descriptive_noun_phrase(pos):
            r_val.append((phrase, pos))
    return r_val

def multiparse(item):
    title,text = item
    print "Computing noun-phrases for", title
    return phrase_block(text)

#word = "Grouse"
#cmd_grab = '''SELECT title, text FROM wiki WHERE title="{}" LIMIT 1'''
#cursor = conn.execute(cmd_grab.format(word))
#print "Searching for {}".format(word)

#cmd_grab = '''SELECT title, text FROM wiki LIMIT 1000'''
cmd_grab = '''SELECT title, text FROM wiki ORDER BY title'''
cursor = conn.execute(cmd_grab)

import codecs
import multiprocessing as mp
P = mp.Pool()

f_raw_np = "gen/raw_NP.txt"

with codecs.open(f_raw_np,'w','utf-8') as FOUT:
    for phrase_list in P.imap(multiparse, cursor):
    #for phrase_list in itertools.imap(multiparse, cursor):
        for phrase,pos in phrase_list:
            str_out = u"{} {}\n".format(phrase, pos)
            #print str_out
            FOUT.write(str_out)

        

        




