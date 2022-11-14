#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# programmation du jeu d'othello 


# ----------------------------- IMPORTATIONS ---------------------------------------

import numpy as np 
from partie import partie 
from MinMax import MinMax

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

partie(False, True)
