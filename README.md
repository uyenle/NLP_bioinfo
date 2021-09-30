# NLP-unstructed-bioinfo
ML learning not only specific relationships of drugs and protein targets but also wider clusters of global thematic relationships


# Structure of process 

Module 1:
- Scrapping Medline abstracts for filtering to search for sentences that contain both a drug and protein known in DrugBank and PharmGKB database.
- Filtered sentences will be parsed to find their dependency path trees in order to  formalize the semantic relationships.
- Building a sparse matrix will be built where each row is a drug-gene relation and each column a potential dependency path. 

Module 2:
- Ensemble Biclustering for Classification (EBC) will be used to bicluster the matrix to yield information on which dependency paths frequently cluster together.        _The assumption is that those paths are likely semantically similar, since their linguistic contexts are similar. The algorithm also yields information on which drug-gene pairs cluster with each other, and this creates an overall ‘landscape’ of interpretable ways that drugs and genes can interact._

Module 3:
- Vizualizing the global sematic relationships by Dendrogam 
