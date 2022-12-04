#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# programmation du jeu d'othello 


# ----------------------------- IMPORTATIONS ---------------------------------------

import numpy as np 
from partie import partie 
from MinMax import MinMax
from alphaBeta import alphaBeta
from MCTS import MCTS

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

ma_partie_ = np.array([[ 2, 2, 2, 0, 0, 0, 0, 2,],[1, 2, 2, 1, 1, 1, 2, 1,],[2, 2, 1, 2, 2, 2, 1, 1,],[2, 2, 1, 2, 2, 2, 1, 1,],[2, 2, 2, 2, 2, 2, 2, 1,],[2, 2, 2, 1, 1, 2, 2, 1,],[2, 2, 1, 1, 2, 2, 2, 1,],[2, 1, 1, 1, 1, 1, 1, 1,]])
#def __init__(self, cases, joueur1,algo_j1,prof_algo_j1, joueur2, algo_j2,prof_algo_j2):
othellier = Othellier(ma_partie_, False,None,1, False, None,1) 
#othellier.fonction_evaluation()
partie(joueur1 = False, algo_j1 = 'MCTS')
'''


print(oth_min_max)
othellier = Othellier(oth_min_max, False, None, 1, True, None, 1) 
minmax = MinMax(othellier, 2, 1, gains = [], chemin = [], profondeurs = [])
print(minmax[0]) # min_score 
print()
print(minmax[1]) # gains
print()
print(minmax[2]) # chemin
print()
print(minmax[3]) # profondeurs 

#partie(False, 'MCTS', True,'minmax')
#partie(False, 'MCTS', 4, True, None, None) 

# rappel des paramètres : 
# partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
'''

