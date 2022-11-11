
# ------------------------------------ IMPORTATIONS ----------------------------------------------------
from othellier import Othellier
import numpy as np 
import copy

# -------------------------------------- MIN MAX ------------------------------------------------

'''
Pour implémenter l'algorithme minMax, nous avons procédé de la manière suivante : 

'''
def genere_successeurs(echiquier): # on fournit en input un objet de classe Othellier
    '''
    Cette fonction génère pour un othellier, tous ses successeurs possibles 
    '''
    successeurs = {} # les successeurs de l'objet donné en input seront sonsignés dans cette liste. 
    pdg = echiquier.fonction_evaluation() # on crée le dictionnaire "promesses de gain" pour l'othellier d'interet 
    for i, case_possible in enumerate(pdg.keys()): 
        # pour chacune des cases possibles, on simule un tour
        cases = copy.deepcopy(echiquier.cases)
        if len(pdg[case_possible]) != 0: 
            # on crée un othellier à partir de celui d'interet 
            i = Othellier(cases, echiquier.joueur, echiquier.adversaire)
            # on le met a jour comme si on avait joué case_possible
            i.mise_a_jour(case_possible, echiquier.a_des_binomes(case_possible)[2])
            i.joueur[0], i.adversaire[0] = i.adversaire[0], i.joueur[0]
            # on l'ajoute à "successeurs" avec sa promesse de gain associée 
            successeurs[i] = i.fonction_evaluation() # NB : il y a alors un dictionnaire dans un dictionnaire 
            
    print(successeurs)
    '''
    print(successeurs[0].cases)
    print()
    print(successeurs[1].cases)
    print()
    print(successeurs[2].cases)
    print()
    print(successeurs[3].cases)
    print(successeurs)
    print(len(successeurs)) 
    '''
    return successeurs

'''
def MinMax(root, prof):

    # Si la branche est terminale 
    if (etage%2) == 0: # si le meud est un maued max, on remont la valeur max des successeurs 
        valeurs_successeurs = []
        pass
        for oth in genere_successeurs(oth_pere):
            valeurs_successeurs.append(oth.fonction_evaluation())
            pass
        remonte = max(valeurs_successeurs)
'''


