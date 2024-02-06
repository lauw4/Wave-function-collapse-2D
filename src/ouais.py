import WFC
import numpy as np

wfc = WFC.WFC("../data/test2.csv", grid_size=(9, 9))
wfc.run_collapse()
g = wfc.grid

g = [[element.pop() for element in row] for row in g]

# Définissez la taille du tableau final n x n
n = 9  # Par exemple, pour un tableau 9x9, remplacez par la valeur souhaitée

# Créez une liste pour stocker les tableaux 3x3
tableaux_3x3 = []

for i in range(n):
    for j in range(n):
        tableau_3x3 = wfc.tiles[g[i][j]].lands_3x3
        tableaux_3x3.append(np.array(tableau_3x3))

# Créez le tableau final n x n rempli de zéros
tableau_final = np.zeros((27, 27), dtype=object)
print(len(tableaux_3x3))
# Remplir le tableau final en utilisant les 91 tableaux 3x3
for i in range(9):
    for j in range(9):
        tableau_final[i*3:(i+1)*3, j*3:(j+1)*3] = tableaux_3x3[i*9 + j]

print(tableau_final)
