#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------- IMPORTATIONS ---------------------------------------

import numpy as np 

from othellier import Othellier
from partie import partie 

from MinMax import MinMax
from alphaBeta import alphaBeta
from MCTS import MCTS

import time

# -------------------------------- Nota Bene --------------------------------------------

# L'othellier est composé de 8 lignes (1-8) et 8 colonnes (a-h). 
# les cases vides sont modélisées par des 0.
# Les pions noirs sont modélisés par des 1 et les pions blancs par des 2. 

# Une partie peut se faire en :
#   - joueur "réel" VS joueur "réel" 
#   - ordinateur avec un algorithme A VS ordinateur avec un algorithem B 
#   - joueur "réel" VS ordinateur avec algorithme 

# -------------------------------- MAIN --------------------------------------------

#Si vous souhaitez lancer une partie avec les paramètres par défaut, vous pouvez exécuter la ligne suivante : 
partie()

'''
# Sinon, vous pouvez les choisir en changeant les lignes suivantes:

# Paramètres de JOUEUR 
j1 = True # Entrez "True" si vous souhaitez jouer, "False" sinon 
algo_1 = None # Si vous avez entré j1 = True, ignorez ce paramètre. Sinon, choisissez un algorithme parmi : 'minmax', 'alphaBeta', None
p1 = None # Si vous avez entré j1 = True, ce paramètre est inutile, ignorez le. Sinon choisissez une profondeur pour l'algorithme choisi. 

# Paramètres de ADVERSAIRE 
j2 = False # Un ordinateur 
algo_2 = 'alphaBeta' # utilisant alphaBeta comme référence 
p2 = 2

# OPTIONNEL 
# Si vous avez choisi d'utiliser MCTS, vous pouvez choisir des paramètres pour c et nombre de "play out":
# Par défaut, dans la classe MCTS, les valeurs sont fixées à 1.414 et 1. 
c = 0.5
nb_po = 2

# La commande suivante lance la partie avec les paramètres choisis. 
partie(joueur1 = j1 , algo_j1 = algo_1, prof_algo_j1 = p1, joueur2 = j2, algo_j2 = algo_2, prof_algo_j2 = p2, valeur_c = c, nb_play_out = nb_po)
# Le terminal vous permettra de visualier le plateau de jeu. 
# Les 0 représentent les cases libres, les 1 et 2 les pions des joueurs noir et blanc. 

'''

