
#%% INITIALIZING 
import numpy as np
# ***** change path to own folder 
from ebc import EBC 
from matrix import SparseMatrix

#%% IMPORTING DENSE MATRIX FROM ORIGINAL PAPER 

with open("/Volumes/PU PU/My Own Code/FINAL/Mo2_EBC/matrix-ebc-paper-dense.tsv", "r") as f:
    data = []
    for line in f:
        sl = line.split("\t")
        if len(sl) < 5:  # headers
            continue
        data.append([sl[0], sl[2], float(sl[4])])

#%% BUILDING CO-OCCURENCY MATRIX FROM EBC PACKAGE

n = 3514      # unique drug-gene pairs
m = 1232      # unique dependency path

matrix = SparseMatrix([n, m]) 
matrix.read_data(data)
matrix.normalize()

Con_mat = np.zeros((n, n), dtype=int) 
#%%
for iter_num in range(100): #original 2000 times
    ebc = EBC(matrix, [30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
    cXY, objective, iter = ebc.run()
    clusters = cXY[0]
    for i in range(n):
        C = clusters[i]
        for j in range(i, n):
            if clusters[j] == C:
                Con_mat[i,j] += 1     # upper triangle of the matrix 
                if i != j: 
                    Con_mat[j,i] += 1   # lower triangle of the matrix without duplicating diagonal

#%% EXPORTING MATRIX
np.savetxt('/Volumes/PU PU/My Own Code/FINAL/Mo2_EBC/Co_mat.txt', Con_mat, delimiter=',')

#%% THE END OF SCRIPT