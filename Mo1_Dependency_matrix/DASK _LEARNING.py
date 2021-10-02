#DASK LEARNING

#1-DASK.BAG 
import dask
from dask.base import visualize
import dask.dataframe as dd
import dask.bag as db
from dask.local import MultiprocessingPoolExecutor
from dask.optimization import default_fused_keys_renamer

import pandas as pd 
import numpy as np
from pandas.core.dtypes.missing import notnull
from pandas.core.frame import DataFrame
from pandas.io.sql import pandasSQL_builder
import spacy #tokennization
import os #interact with operating system 
import regex as re # check if a string contains the specified search pattern
import xml.etree.ElementTree as et 

import pubmed_parser as pp #read Medline data 
import requests
import graphviz #assemble the graph by nodes and edges
from gzip import decompress

#%%
pubmed_paths = ["data/pubmed21n" + str(num).zfill(4) + '.xml'  for num in range(1,3)]
print(pubmed_paths)

def convert_xml_to_csv(xml_file):
    csv_file = pd.DataFrame.from_dict(pp.parse_medline_xml(xml_file))
    csv_file.to_csv(path_or_buf = re.sub(r'.xml', r'.csv', xml_file), index = False)
    pass 
for xml_file in pubmed_paths:
    convert_xml_to_csv(xml_file)

b = db.from_sequence(pubmed_paths).map(convert_xml_to_csv)
#%%
# length of each bag 
b.map(len).compute()
#%%
b.map(type).compute()
#%%
b_filtfred = b.map(lambda df: df((df('abstract').notnull()) & (df('abstract') != u'')))
b_filtfred.visualize()
#%%  
b_filtfred = b_filtfred.compute()
# %%
type(b_filtered[0]).head() 


# %%
from dask.MultiprocessingPoolExecutor import get

def load(xml_file):
    return pd.DataFrame.from_dict(pp.parse_medline_xml(xml_file))

def clean(df):
    return df((df('abstract').notnull()) & (df('abstract') != u''))) 

def analyze(df):
    return (len(i) for i in df)

def store(results):
    with open('data/text_data.txt', 'w') as f:
        f.write(str(results))


graph = {'parse_xml-1': (load, pubmed_paths[0]),
    'parse_xml-2': (load, pubmed_paths[1],
    'filter_abstact-1': (clean,'parse_xml-1' ),
    'filter_abstact-2': (clean,'parse_xml-2' ),
    'get_len': (analyze, ['filter_abstact-%d' i for i in [1,2]]),
    'store': (store, 'get_len')}


dask.visualize(graph)   



#2-DASK.DATAFRAME 

#%% 
df = dd.read_csv('data/pubmed21*.csv',  dtype={'abstract': 'object',
       'affiliations': 'object',
       'keywords': 'object',
       'nlm_unique_id': 'object',
       'other_id': 'object',
       'pmc': 'object'})
#dask's dtype inference failing, and may be fixed by specifying dtypes manually
df.head()
# %%
#filter for those with non-NaN abstract
df_filtered = df[df.abstract.notnull()]
df_filtered.head()
# %%
df_filtered.compute()
#%%
df_filtered.map_partitions(len).compute()
