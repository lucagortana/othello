
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

def valeur_dico(position, dict):
    compteur = -1
    for element in dict.items():
        compteur += 1
        if compteur == position:
            return element

def MinMax(root, prof):
    level = 0 #nous sommes à la racine
    compteur = 0 #compteur nous permettant de ne pas explorer à chaque boucle while TOUS les noeuds, mais seulement les plus profonds
    gain_noeud = {} 
    gain_noeud[(0,0)] = [(0, len(element[1])) for element in root.fonction_evaluation().items()] #on crée un dico donnant le gain associé à chaque noeud (au début, chaque noeud a un gain de 0)
    othellier_noeud = {}
    othellier_noeud[root] = (0, 0) #on crée un dico qui donne à chaque othellier généré son noeud associé
    level = 1 #on passe au niveau supérieur
    while level < prof: #tant que nous n'avons pas atteint les feuilles, nous continuons de générer des othelliers en retenant pour chacun leur noeud
        for i in range(compteur, len(othellier_noeud)): #pour chaque othellier de la couche d'avant
            nexts = genere_successeurs(valeur_dico(i, othellier_noeud)[0]) #on génère les successeurs de cet othellier
            compteur += 1
            branche = 0 #on initialise à la branche 0.
            for oth_genere in nexts.items(): #pour chaque othellier généré
                nv_oth = oth_genere[0]
                othellier_noeud[nv_oth] = (level, branche) #on rajoute à la liste othellier_noeud l'othellier et le noeud associé
                gain_noeud[(level, branche)] = (0, max([len(element[1]) for element in nv_oth.fonction_evaluation().items()]))
                branche += 1 
    level += 1
    pass #à suivre

#successeurs = {oth_genere1: {position_possibles: cases retournables},
#               oth_genere2: {position_possibles: cases retournables}}
