# %% SIMULATION 
import time
import numpy as np 
from partie import partie 
import pandas as pd
from math import sqrt

import matplotlib.pyplot as plt 


#-------------------------------------- FIGHTS DES ALGOS -----------------------------

# on va faire affronter 2 ordinateurs au cours de nb_parties. 
# Ordinateur 1 joue selon l'algorithme algo_1 de profondeur p1, l'autre avec algo_2 de profondeur p2.
# On enregistre pour chaque ordinateur et chaque profondeur testée le nb de parties gagnées, pour ensuite résliser une étude statistique 
nb_parties = 40

# algo de reference = JOUEUR A 
algo_1 = 'ref'
p1 = 1

# algo que l'on va tester = JOUEUR B 
algo_2 = 'alphaBeta'
#p= 2

# utile pour MCTS 
#c = 1
#nb_po = 4 

prof_test = {}
for p in [1,2,3]:

    print('nous en sommes à la profondeur {p}'.format(p=p))

    start_time = time.time()
    gain_A = 0
    gain_B = 0
    egalite = 0

    for i in range(nb_parties):
        print('nous en sommes à la partie ', i)

        if i%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
            #print('Joueur_A commence')
            gagnant = partie(joueur1 = False , algo_j1 = algo_1, prof_algo_j1 = p1, joueur2 = False, algo_j2 = algo_2, prof_algo_j2 = p)
            # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
            if gagnant == 1:
                gain_A += 1
            elif gagnant == 2:
                gain_B += 1
            else:
                egalite += 1 
        

        if i%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
            #print('Joueur_B commence')
            gagnant = partie(joueur1 = False , algo_j1 = algo_2, prof_algo_j1 = p, joueur2 = False, algo_j2 = algo_1, prof_algo_j2 = p1)
            
            if gagnant == 1:
                gain_B += 1
            elif gagnant == 2:
                gain_A += 1
            else:
                egalite += 1 

    #prof_test[p_o] = gain_A/nb_parties , gain_B/nb_parties, egalite/nb_parties # %ages de parties gagnée , perdue , egalité 
    #print("gain_B/nb_parties", gain_B/nb_parties)
    print("--- %s seconds ---" % (time.time() - start_time))
    prof_test[p] = gain_A/nb_parties , gain_B/nb_parties, egalite/nb_parties # %ages de parties gagnées , perdues , egalité 


# Les valeurs que nous allons entrer pour l'histogramme :
x = [key for key in prof_test.keys()]
#x = [1,5,10]
#print(x)
#x = [1,2,3]
y_A = [value[0] for value in prof_test.values()]
y_B = [value[1] for value in prof_test.values()]
y_eg = [value[2] for value in prof_test.values()]

# calcul des intervalles de confiance à 95% 
IC_95_B = []
for p in range(len(y_B)):
    prop = y_B[p] # une valeur moyenne pour chaque profondeur 
    IC_95_B.append((1.96 * sqrt( (prop*(1-prop))/nb_parties)))

IC_95_A = []
for p in range(len(y_A)):
    prop = y_A[p] # une valeur moyenne pour chaque profondeur 
    IC_95_A.append((1.96 * sqrt( (prop*(1-prop))/nb_parties)))

IC_95_E = []
for p in range(len(y_eg)):
    prop = y_eg[p] # une valeur moyenne pour chaque profondeur 
    IC_95_E.append((1.96 * sqrt((prop*(1-prop))/nb_parties)))

legende = {"{algo_1}".format(algo_1 = algo_1): 'green', "{algo_2}".format(algo_2 = algo_2): 'red'}        
labels = list(legende.keys())
handles = [plt.Rectangle((0,0),1,1, color=legende[label]) for label in labels]

plt.figure()
plt.bar(np.array(x)-0.2,y_A,0.2, color = 'g')
plt.bar(np.array(x),y_B,0.2, color = 'r') #, tick_label = C)
plt.bar(np.array(x)+0.2,y_eg,0.2, color = 'b')
plt.xlabel('profondeur')
#plt.title('Profondeur = 10')
#plt.xlabel('nombre de play out')
plt.ylabel('Ratio de parties gagnées')
#plt.title('Performance de alphaBeta selon la profondeur')
#plt.text(0.8, 0.95, 'nombre de parties = {nbp}'.format(nbp = nb_parties))
#plt.xlim(0, p2+1)
#plt.xticks(x)
#plt.xticks([1, 5, 10])
#plt.xlim(0,6)
plt.ylim(0, 1)
plt.grid(False)
plt.legend(handles, labels)
plt.errorbar(np.array(x) - 0.2, y_A, yerr = abs(np.array(IC_95_A)), fmt = 'None', ecolor='k', capsize=5)
plt.errorbar(np.array(x), y_B, yerr = abs(np.array(IC_95_B)),fmt = 'None', ecolor='k', capsize=5)
plt.errorbar(np.array(x)+0.2, y_eg, yerr = abs(np.array(IC_95_E)) ,fmt = 'None', ecolor='k', capsize=5)
plt.savefig('resultats_simulations/{algo1}_{algo2}_ndp_{nb_parties}'.format(algo1 = algo_1, algo2 = algo_2, nb_parties = nb_parties))

plt.show()


# %%
