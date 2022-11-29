#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# programmation du jeu d'othello 


# ----------------------------- IMPORTATIONS ---------------------------------------

import numpy as np 
from partie import partie 
from MinMax import MinMax
from alphaBeta import alphaBeta

import time

# -------------------------------- MAIN --------------------------------------------

# L'othellier est composé de 8 lignes (1-8) et 8 colonnes (a-h). 
# les cases vides sont modélisées par des 0.
# Les pions noirs sont modélisés par des 1 et les pions blancs par des 2. 


# Une partie peut se faire en 1 VS 1 ou par l'ordi contre lui même ou en joueur VS ordi. 
# Si joueur_n = True --> joueur_n est une personne réelle.
# Si joueur_n = False --> joueur_n = ordinateur 

# Par défaut, joueur1 = True et joueur2 = False 

#partie(False, False)


# ____________ 

from othellier import Othellier

oth_min_max = np.zeros([8,8]) 
oth_min_max[4,3] = 1    
oth_min_max[3,4] = 1 
oth_min_max[3,3] = 2   
oth_min_max[4,4] = 2   
oth_min_max[3,2] = 1   
oth_min_max[2,2] = 2

#print(oth_min_max)
#othellier = Othellier(oth_min_max, False, True) 
#minmax = MinMax(othellier, 3, 1, gains = [], chemin = [], profondeurs = [])

#partie(False, 'minmax', True,'minmax')


#-------------------------------------- FIGHTS DES ALGOS -----------------------------
start_time = time.time()

# on va faire affronter 2 ordinateurs au cours de 10 parties. 
# Un avec Minmax, l'autre en choix random.
# on va voir qui gagne le plus de parties. 
prof_test = {}
for p in range(1,3):
    print('nous en sommes à la profondeur {p}'.format(p=p))

    gain_A = 0
    gain_B = 0
    egalite = 0

    for nb_partie in range(3):
        print('nb_partie=', nb_partie)

        joueur_A = None
        joueur_B = 'alphaBeta'

        if nb_partie%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
            print('Joueur_A commence')
            #gagnant = partie(False, None, 1, False, joueur_B, p) 
            gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 1, joueur2 = False, algo_j2 = 'alphaBeta', prof_algo_j2 = p)
            # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
            
            if gagnant == 1:
                gain_A += 1
            elif gagnant == 2:
                gain_B += 1
            else:
                egalite += 1 

        if nb_partie%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
            print('Joueur_B commence')
            gagnant = partie(False, joueur_B,1, False, None, p)
            
            if gagnant == 1:
                gain_B += 1
            elif gagnant == 2:
                gain_A += 1
            else:
                egalite += 1 

    print(gain_A)
    print(gain_B)
    print(egalite)

    prof_test[p] = gain_A , gain_B  

# faire un histogramme à partir du dictionnaire prof_test : en abscisse les profondeurs 
# pour chaque profondeur 2 barres : une pour "parties gagnées par A et l'autre parties gagnées par B 
# # ou alors : une seule barre avec la difference gain A - B"
print("--- %s seconds ---" % (time.time() - start_time))

print(prof_test)