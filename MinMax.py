
# ------------------------------------ IMPORTATIONS ----------------------------------------------------
from othellier import Othellier
import numpy as np 
import copy

# -------------------------------------- MIN MAX ------------------------------------------------

def MinMax(othellier, prof, min_ou_max, gains, chemin, profondeurs):
    '''
    othellier = l'othellier pour lequel  on veut faire l'évaluation
    prof = la profondeur jusqu'à laquelle on veut réaliser l'algorithme minmax
    min_ou_max = 1 ou 2, pour savoir si le noeud est un noeud min ou un noeud max 
    "gains", "chemin" et "profondeurs" sont des listes vides au début de l'algorithme. 
    À chaque boucle dans l'algorithme elles se remplissent. 
    "gains", "chemin" et "profondeurs" sont les outputs de minmax.
    À elles trois, ces listes sont une reconstitution de l'arbre.
    '''

    cases_possibles = othellier.promesses_de_gain().keys() # on va envisager toutes les possibilités de jeu (= facteur de branchement)
    # on "recopie" le plateau de l'othellier de départ, sinon les modifications se font sur cet othellier de départ ! 

    max_score = -1000 # initialisation --> le max score sera forcément meilleur que ça 
    min_score = 1000 # initialisation 

    # si on est au niveau d'une feuille, on return la valeur de la fonction d'évaluation
    # NB : (np.where(othellier.cases == 0, 10, 0).sum() == 0) signifie qu'il n'y a a plus de cases libres 
    if prof == 0 or np.where(othellier.cases == 0, 10, 0).sum() == 0: 

        #gains.append(np.where(othellier.cases == 1, True, False).sum() - np.where(othellier.cases == 2, True, False).sum())
        return othellier.fonction_evaluation()

    # Dans le cas où le noeud n'est pas terminal, on réapplique la fonction MinMax sur ses successeurs possibles 
    if othellier.joueur[0] == min_ou_max: #min_ou_max vaut soit 1 soit 2 selon quel joueur on souhaite maximiser
        for case in cases_possibles:
            # on crée le nouvel othellier qui découlerait de ce choix de case : 
            oth_fils = copy.deepcopy(othellier)
            oth_fils.mise_a_jour(case, othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur

            # on enregistre la valeur que cet othellier nous rapporterait 
            score = MinMax(oth_fils, prof - 1, min_ou_max, gains, chemin, profondeurs )[0]
            gains.append(score)
            chemin.append(case)
            profondeurs.append(prof)
            max_score = max(score, max_score)
 
        return max_score , gains , chemin , profondeurs 
    
    else: # idem que précédemment, mais pour un noeud min 
        for case in cases_possibles:
            oth_fils = copy.deepcopy(othellier) 
            oth_fils.mise_a_jour(case, othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur    

            # on enregistre la valeur que cet othellier nous rapporterait si la case était jouée  
            score = MinMax(oth_fils, prof - 1, min_ou_max, gains, chemin, profondeurs)[0]
            gains.append(score)
            chemin.append(case)
            profondeurs.append(prof)
            min_score = min(min_score, int(score))

        return min_score , gains, chemin , profondeurs 


# --------------------- à conserver ???? 

def genere_successeurs(echiquier): # on fournit en input un objet de classe Othellier
    '''
    Cette fonction génère pour un othellier donné, tous ses successeurs possibles 
    '''
    successeurs = {} # les successeurs de l'objet donné en input seront sonsignés dans cette liste. 
    pdg = echiquier.promesse_de_gain() # on crée le dictionnaire "promesses de gain" pour l'othellier d'interet 
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
            successeurs[i] = i.promesses_de_gain() # NB : il y a alors un dictionnaire dans un dictionnaire 
            
    print(successeurs)
    return successeurs