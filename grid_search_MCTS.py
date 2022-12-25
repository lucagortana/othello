import time
import numpy as np 
from partie import partie 
import pandas as pd
from math import sqrt

import matplotlib.pyplot as plt 


## "grid search" : Variations des paramètres C et play out : quelle est la meilleure combinaison possible ?

nb_parties = 30
# algo de reference = JOUEUR A 
algo_1 = None
p1 = 1
# algo que l'on va tester = JOUEUR B 
algo_2 = 'MCTS'
p2 = 3

C = [0.01, 1.414, 5, 10]
p_o = [1,  4 , 10]
#res = pd.DataFrame(columns=C, index = p_o)
res = np.zeros([len(p_o), len(C)])
print(res)
for i in range(len(C)):
    for j in range(len(p_o)):

        print("Nous testons la combinaison (c, po) = ", C[i], p_o[j])

        start_time = time.time()
        gain_A = 0
        gain_B = 0
        egalite = 0

        for k in range(nb_parties):
            print('nous en sommes à la partie ', k)

            if i%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
                #print('Joueur_A commence')
                gagnant = partie(joueur1 = False , algo_j1 = algo_1, prof_algo_j1 = p1, joueur2 = False, algo_j2 = algo_2, prof_algo_j2 = p2, valeur_c = C[i], nb_play_out = p_o[j])
                # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
                if gagnant == 1:
                    gain_A += 1
                elif gagnant == 2:
                    gain_B += 1
                else:
                    egalite += 1 
            

            if i%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
                #print('Joueur_B commence')
                gagnant = partie(joueur1 = False , algo_j1 = algo_2, prof_algo_j1 = p2, joueur2 = False, algo_j2 = algo_1, prof_algo_j2 = p1, valeur_c = C[i], nb_play_out = p_o[j])
                
                if gagnant == 1:
                    gain_B += 1
                elif gagnant == 2:
                    gain_A += 1
                else:
                    egalite += 1 

        print("--- %s seconds ---" % (time.time() - start_time))
        #print(res.loc[po, c])
        #(gain_A/nb_parties , gain_B/nb_parties, egalite/nb_parties) 
        res[j][i] = gain_B/nb_parties # %ages de parties gagnées , perdues , egalité 
        print(res)


# On représente maintenant les résultats sous forme de Heatmap : 

fig, ax = plt.subplots(figsize=(8,8))
im = ax.imshow(res, cmap = 'YlOrRd') 
cbar = ax.figure.colorbar(im, ax=ax ,shrink=0.5 )
plt.xlabel('valeur de C')
plt.ylabel('valeur de play_out')
#plt.xlim(0, 1)
#plt.ylim(p_o[0], p_o[-1])
ax.set_xticks(np.arange(len(C)), labels = C)
ax.set_yticks(np.arange(len(p_o)), labels = p_o)
#ax.set_yticks(p_o)
#plt.xscale('log')
#ax.grid(True)
fig.tight_layout()
plt.show()

'''
[[0.75  0.625 0.675 0.65 ]
 [0.75  0.775 0.6   0.75 ]
 [0.775 0.7   0.775 0.65 ]
 [0.625 0.75  0.725 0.675]
 [0.7   0.675 0.725 0.6  ]]
'''


