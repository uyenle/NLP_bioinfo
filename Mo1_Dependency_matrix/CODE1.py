#%% INITIALIZING 
import requests
import pubmed_parser as pp
import pandas as pd
from gzip import decompress
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
#nltk.download("punkt")

#%% DOWNLOADING FILES .XML.GZ FROM MEDLINE 
SIZE = 5 # how many files are downloaded
parsed_files = []
fnames = ["pubmed21n" + str(num).zfill(4) + ".xml" for num in range(1,1 + SIZE)]

# getting + processing files
ftp_url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
for fname in fnames:
    r = requests.get(ftp_url + fname + '.gz')
    data = decompress(r.content)
    medline_data = pd.DataFrame.from_dict(pp.parse_medline_xml(data))
    medline_data = medline_data[['abstract', 'pubdate']]
    parsed_files.append(medline_data)
    print('appended')

pubmed_df = pd.concat(parsed_files, ignore_index=True)


#%% CLEANING ABSTRACTS TO BE USED 
pubmed_df = pd.read_csv("/Volumes/PU PU/My Own Code/FINAL/Mo1_Dependency_matrix/pubmed_df.tsv", sep = '\t')

#drop null abstracth
pubmed_df = pubmed_df.dropna(axis=0)

#only working with data before 2015
abstracts = [pubmed_df['abstract'][i] for i in pubmed_df.index if int(pubmed_df['pubdate'][i]) <= 2015] 
#%% BENCHMARK DATA FROM PHARMGKB AND DRUGBANK(****** add data from drugbank to drugs)
#drugbank_drug = pd.read_csv('/Volumes/PU PU/My Own Code/data/drugbank_name.csv') 
drug_name = pd.read_csv('/Volumes/PU PU/My Own Code/FINAL/Mo1_Dependency_matrix/drugs.tsv', sep = '\t')
drugs = []
drugs.extend(drug_name["Name"])
gene_name = pd.read_csv('/Volumes/PU PU/My Own Code/FINAL/Mo1_Dependency_matrix/genes.tsv', sep= '\t')
genes =[]
genes.extend(gene_name['Name'])

set_drugs = set(drugs)
set_genes = set(genes)

#%% TOKENIZING SENTENCES IN ABSTRACTS
sentences = []
for abstract in abstracts:
    sentences += nltk.tokenize.sent_tokenize(abstract)
    #words += nltk.word_tokenize(abstract)


#%% NARROWING DOWN TO SENTENCES THAT CONTENTING KNOWN DRUG AND GENE FROM PHARMGKB AND DRUGBANK 
usable_sentences = []

for sentence in sentences:
    drug, gene = False, False
    genename =''
    token_sentence = nltk.tokenize.word_tokenize(sentence)
    for token in token_sentence:
        if token in set_drugs:
            drug = True
        if token in set_genes:
            gene = True
        if drug and gene:
            usable_sentences.append(sentence)
            break

#%% SAVING SENTENCES 
file = open("/Volumes/PU PU/My Own Code/data/original/usable_sentences.tsv", "w", encoding='utf-8')
file.write('\t'.join(usable_sentences))
file.close()
print('done')

#IN STANFORD FOLDER (*** SHOULD BE CHANGE PATHNAME)
file = open("//Volumes/PU PU/My Own Code/stanford-parser-full-2014-10-31/mydata/usable_sentences.tsv", "w", encoding='utf-8')
file.write('\t'.join(usable_sentences))
file.close()
print('done')

#%% run in terminal 
#java -cp '*' -mx500m edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "wordsAndTags,penn,typedDependencies" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz mydata/



#%% IMPORT STANFORD PARSER OUTPUT
infile = open('/Volumes/PU PU/My Own Code/FINAL/Mo1_Dependency_matrix/stanford-parser-full-2014-10-31/mydata/out_put.txt', 'r')
#%% GETTING THE DEPENDENCY PATHS BETWEEN DRUG AND GENE
dependencies = []

for line in infile:
    if line[0].islower() and line.find('(') != -1:
        stripline = line[line.find('(') + 1 : line.find(')')]
        stripline = stripline.split(', ')
        for i in range(2):
            stripline[i] = stripline[i][:stripline[i].rfind('-')]
        drug, gene = '', ''
        for word in stripline:
            if word in set_drugs:
                drug = word
            elif word in set_genes:
                gene = word
        if drug and gene:
            dependencies.append((line[:line.find('(')], (drug, gene)))




# %% BUILDING DEPENDENCY MATRIX
# nrow = numbers of unique drug-gene pairs
# ncol = numbers of unique dependency paths 
import numpy as np 
setrelations = set()
setpairs = set()
for dependency in dependencies:
    setrelations.add(dependency[0])
    setpairs.add(dependency[1])
relations = list(setrelations)
pairs = list(setpairs)
#%%
zeroes = np.zeros(shape=(len(pairs), len(relations)))
matrix = pd.DataFrame(zeroes, index = pairs, columns = relations)
for dependency in dependencies:
    matrix.at[dependency[1], dependency[0]] += 1

#%% 
# Counting unique values of pairs and paths 
freq = pd.DataFrame(columns=['paths', 'pairs'], data=dependencies)
fpairs = freq.groupby('pairs').count()
fpaths = freq.groupby('paths').count()

#%% THE END OF SCRIPT 