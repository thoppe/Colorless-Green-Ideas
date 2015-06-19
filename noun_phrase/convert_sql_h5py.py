import sqlite3
import pandas as pd
import numpy as np
import h5py

f_h5 = "JJ_noun_phrase.h5"

f_db = "JJ_noun_phrase.db"
conn = sqlite3.connect(f_db)

h5 = h5py.File(f_h5, 'w')

nouns = pd.read_sql("SELECT * FROM PCA_nouns",conn,index_col="index")
g = h5.create_group("nouns")
g.create_dataset("words", data=np.array(nouns.index,dtype='S20'))
g.create_dataset("svd", data=nouns.values)

adjs  = pd.read_sql("SELECT * FROM PCA_adjs", conn,index_col="index")
g = h5.create_group("adjs")
g.create_dataset("words", data=np.array(adjs.index,dtype='S20'))
g.create_dataset("svd", data=adjs.values)

var   = pd.read_sql("SELECT * FROM PCA_explained_variance", 
                    conn,index_col="index")
h5.create_dataset("variance", data=var.values)
